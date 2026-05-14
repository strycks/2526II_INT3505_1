from flask import Response
from flask_restx import Resource, Namespace
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

ns_metrics = Namespace('metrics')

@ns_metrics.route('')
@ns_metrics.doc(security=[])
class Metrics(Resource):
    def get(self):
        """Expose Prometheus metrics for scraping."""
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)