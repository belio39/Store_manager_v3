import os
from flask_jwt_extended import JWTManager
from app.models import DatabaseDriver
from app import APP

APP.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(APP)

if __name__ == '__main__':
  APP.run(debug=True)