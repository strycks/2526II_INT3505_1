import time
from functools import wraps
import uuid
from flask import g, request
from prometheus_client import Counter, Histogram, Gauge
import logging

logger = logging.getLogger(__name__)

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

    @app.before_request
    def before_request():
        g.request_start_time = time.perf_counter()
        g.trace_id = str(uuid.uuid4())
        endpoint = request.endpoint or 'unknown'
        IN_PROGRESS_REQUESTS.labels(method=request.method, endpoint=endpoint).inc()
        logger.info(f"Request started: {request.method} {request.path} - Trace ID: {g.trace_id}")

    @app.after_request
    def after_request(response):
        endpoint = request.endpoint or 'unknown'
        elapsed = time.perf_counter() - getattr(g, 'request_start_time', time.perf_counter())
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(elapsed)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=str(response.status_code)).inc()
        IN_PROGRESS_REQUESTS.labels(method=request.method, endpoint=endpoint).dec()
        response.headers['X-Trace-ID'] = getattr(g, 'trace_id', 'unknown')
        logger.info(f"Request completed: {request.method} {request.path} - Status: {response.status_code} - Trace ID: {getattr(g, 'trace_id', 'unknown')} - Duration: {elapsed:.4f}s")
        return response

    @app.teardown_request
    def teardown_request(exc):
        if exc is not None and hasattr(g, 'request_start_time'):
            endpoint = request.endpoint or 'unknown'
            IN_PROGRESS_REQUESTS.labels(method=request.method, endpoint=endpoint).dec()
            logger.error(f"Request failed: {request.method} {request.path} - Trace ID: {getattr(g, 'trace_id', 'unknown')} - Error: {str(exc)}")
