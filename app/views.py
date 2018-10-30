import re
from datetime import datetime as dt
from datetime import timedelta

from flask import request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt import JWT
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import CONNECTION, APP
from app.models import Users

cursor = CONNECTION.cursor()

@APP.route('/api/v2/auth/signup', methods=['POST'])
@jwt_required  
def register_user():
  """Register New User"""
  if request.json and \
  request.json['username'] and \
  request.json['email'] and \
  request.json['password']:
    current_user = get_jwt_identity()
    if str(current_user[5]) == 'True':
      email = request.json['email']
      username = request.json['username']
      password = request.json['password']
      isadmin = request.json.get('isadmin', False)
      email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"
      date = dt.now()
      if re.match(email_format, email):
        username_format = r"(^[a-zA-z0-9_.]*$)"
        if re.match(username_format, username):
          sql = 'SELECT * FROM users WHERE email=%s;'
          cursor.execute(sql, ([email]))
          existing = cursor.fetchall()
          if not existing:
            sql = 'INSERT INTO users(username, email, password, created_on, isadmin) VALUES(%s, %s, %s, %s, %s);'
            password_hashed = generate_password_hash(password)
            cursor.execute(sql, (username, email, password_hashed, date, isadmin))
            CONNECTION.commit()
            return jsonify({"message":"User created successfully"}), 201
          return make_response(jsonify({"message":"The email is already registered"})), 400
        return jsonify({"message":"Username should contain alphanumeric values only"}), 400
      return jsonify({"message":"Invalid email format"}), 400
    return jsonify({"message": "Admin route"})
  return abort(400), 400

@APP.route('/api/v2/auth/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
      return jsonify({'message': 'Please provide email and password'}), 400
    if not re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", email):
      return jsonify({"message": "Invalid email format"}), 400
    cursor.execute('SELECT * FROM users WHERE email=%s;', [email,])
    user = cursor.fetchone()
    if user:
        if check_password_hash(user[3], password):
            access_token = create_access_token(identity=user, expires_delta=timedelta(days=30))
            return jsonify({"access_token": access_token, "message": "logged in successfully"}), 200
        return jsonify({"message": "invalid  credentials"}), 400
    return jsonify({"message": "invalid  credentials"}), 400


      