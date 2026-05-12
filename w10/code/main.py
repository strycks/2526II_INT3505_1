from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect, disconnect
from apis import blueprint_v1, blueprint_v2
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "tXHzZyrglpWqIgfONgcI+gsoCnXKhFFRsFsLtfx0JqU="
jwt = JWTManager(app)
connect(host=os.getenv("MONGODB_URI"))
app.register_blueprint(blueprint_v1)
app.register_blueprint(blueprint_v2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)