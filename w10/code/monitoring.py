import os
import sys
import time
import uuid
import logging
from flask import g, request
from prometheus_client import Counter, Histogram, Gauge
import requests

logger = logging.getLogger(__name__)


class LokiHandler(logging.Handler):
    def __init__(self, url, labels=None, auth=None, timeout=5, verify=True):
        super().__init__()
        self.url = url
        self.labels = labels or {}
        self.auth = auth
        self.timeout = timeout
        self.verify = verify

    def emit(self, record):
        try:
            timestamp_ns = str(int(time.time() * 1e9))
            message = self.format(record)
            stream_labels = {k: str(v) for k, v in self.labels.items()}
            payload = {
                'streams': [
                    {
                        'stream': stream_labels,
                        'values': [[timestamp_ns, message]]
                    }
                ]
            }
            response = requests.post(
                self.url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                auth=self.auth,
                timeout=self.timeout,
                verify=self.verify
            )
            if response.status_code >= 300:
                # Log error without calling handleError to avoid traceback issues
                print(f"Loki push failed: {response.status_code} - {response.text}", file=sys.stderr)
        except Exception as e:
            # Log error without calling handleError
            print(f"Loki push exception: {e}", file=sys.stderr)

REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)
IN_PROGRESS_REQUESTS = Gauge(
    'app_requests_in_progress',
    'Current in-progress HTTP requests',
    ['method', 'endpoint']
)
APP_INFO = Gauge(
    'app_info',
    'Application information',
    ['version']
)


def init_app(app):
    APP_INFO.labels(version='1.0.0').set(1)

    root_logger = logging.getLogger()

    loki_url = os.getenv('LOKI_URL')
    if loki_url:
        loki_labels = {
            'app': os.getenv('LOKI_APP_NAME', 'soa-app'),
            'environment': os.getenv('ENVIRONMENT', 'development'),
            'service': os.getenv('LOKI_SERVICE', 'soa-api')
        }
        loki_handler = LokiHandler(
            url=loki_url,
            labels=loki_labels,
            auth=None,
            timeout=5,
            verify=True
        )
        loki_handler.setLevel(logging.INFO)
        loki_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(loki_handler)
        logger.info(f"Loki logging enabled: {loki_url}")

    @app.before_request
    def before_request():
        g.request_start_time = time.perf_counter()
        endpoint = request.endpoint or 'unknown'
        IN_PROGRESS_REQUESTS.labels(method=request.method, endpoint=endpoint).inc()
        trace_id = request.headers.get('X-Trace-ID') or str(uuid.uuid4())
        logger.info(f"Request started: {request.method} {request.path} - Trace ID: {trace_id}")

    @app.after_request
    def after_request(response):
        endpoint = request.endpoint or 'unknown'
        elapsed = time.perf_counter() - getattr(g, 'request_start_time', time.perf_counter())
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(elapsed)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=str(response.status_code)).inc()
        IN_PROGRESS_REQUESTS.labels(method=request.method, endpoint=endpoint).dec()
        trace_id = request.headers.get('X-Trace-ID') or str(uuid.uuid4())
        response.headers['X-Trace-ID'] = trace_id
        logger.info(
            f"Request completed: {request.method} {request.path} - Status: {response.status_code} - "
            f"Trace ID: {trace_id} - Duration: {elapsed:.4f}s"
        )
        return response

    @app.teardown_request
    def teardown_request(exc):
        if exc is not None and hasattr(g, 'request_start_time'):
            endpoint = request.endpoint or 'unknown'
            IN_PROGRESS_REQUESTS.labels(method=request.method, endpoint=endpoint).dec()
            trace_id = request.headers.get('X-Trace-ID') or str(uuid.uuid4())
            logger.error(
                f"Request failed: {request.method} {request.path} - Trace ID: {trace_id} - Error: {str(exc)}"
            )
