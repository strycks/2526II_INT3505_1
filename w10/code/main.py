from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mongoengine import connect, disconnect
from apis import api
import os
import logging
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics
import monitoring
from limiter import limiter

load_dotenv()

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log', encoding='utf-8')  # Log to file
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize rate limiter
limiter.init_app(app)

metrics = PrometheusMetrics(app=app, path=None)
monitoring.init_app(app)

app.config["JWT_SECRET_KEY"] = "tXHzZyrglpWqIgfONgcI+gsoCnXKhFFRsFsLtfx0JqU="
jwt = JWTManager(app)

connect(host=os.getenv("MONGODB_URI"))

api.init_app(app)

logger.info("Application started successfully")

if __name__ == "__main__":
    logger.info("Starting Flask app on host 0.0.0.0 port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)