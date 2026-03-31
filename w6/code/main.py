from flask import Flask
from flask_jwt_extended import JWTManager
from apis import api
from database import init_db

init_db()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "tXHzZyrglpWqIgfONgcI+gsoCnXKhFFRsFsLtfx0JqU=" 
jwt = JWTManager(app)
api.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)