import re
from datetime import datetime as dt
from datetime import timedelta

from flask import request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt import JWT
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import CONNECTION, APP
from app.models import Users, Products

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
def login_user():
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

@APP.route('/api/v2/products', methods=['POST'])
@jwt_required
def post_product():
    data = request.json.get
    name = data('name')
    quantity = data('quantity')
    price = data('price')
    date = dt.now()
    if not request.json:
        return jsonify({'message': 'Data must be in jsonify'}), 400
    if not name or not quantity or not price:
        return jsonify({'message': 'Name, quantity and price should not be empty.'}), 400
    if not name.isalnum():
        return jsonify({'message': 'Name contains only numbers'}), 400
    if not quantity.isnumeric():
        return jsonify({'message': 'Quantity contains only numbers'}), 400
    if not price.isnumeric():
        return jsonify({'message': 'Price contains only numbers'}), 400
    if not name.isalnum():
        return jsonify({'message': 'Name contains only alphabets or numbers'}), 400
    sql = 'SELECT * FROM products WHERE name=%s;'
    cursor.execute(sql, ([name]))
    existing = cursor.fetchall()
    if not existing:
        sql = 'INSERT INTO products(name, quantity, price, created_on) VALUES(%s, %s, %s, %s);'
        cursor.execute(sql, (name, quantity, price, date))
        CONNECTION.commit()
        return jsonify({"message":"product created successfully"}), 201
    return jsonify({"message": "That product already exists"})

@APP.route('/api/v2/products/<int:product_id>', methods=['PUT'])
@jwt_required
def edit_product(product_id):
    data = request.json.get
    name = data('name')
    quantity = data('quantity')
    price = data('price')
    if not request.json:
        return jsonify({'message': 'Data must be in jsonify'}), 400
    if not name or not quantity or not price:
        return jsonify({'message': 'Name, quantity and price should not be empty.'}), 400
    if not name.isalnum():
        return jsonify({'message': 'Name contains only numbers'}), 400
    if not quantity.isnumeric():
        return jsonify({'message': 'Quantity contains only numbers'}), 400
    if not price.isnumeric():
        return jsonify({'message': 'Price contains only numbers'}), 400
    if not name.isalnum():
        return jsonify({'message': 'Name contains only alphabets or numbers'}), 400
    sql = 'UPDATE products SET name=%s, price=%s, quantity=%s WHERE product_id=%s;'
    cursor.execute(sql, (name, price, quantity, product_id))
    CONNECTION.commit()
    return jsonify({"message":"Product updated successfully"}), 201

@APP.route('/api/v2/products/', methods=['GET'])
@jwt_required
def get_products():
    sql = 'SELECT * FROM products ORDER BY product_id;'
    cursor.execute(sql)
    products = cursor.fetchall()
    return jsonify({"products": products})


@APP.route('/api/v2/products/<int:product_id>', methods=['GET'])
@jwt_required
def get_product(product_id):
    sql = 'SELECT * FROM products WHERE product_id=%s;'
    cursor.execute(sql, ([product_id]))
    product = cursor.fetchall()
    return jsonify({"products": product})

@APP.route('/api/v2/products/<int:product_id>', methods=['DELETE'])
@jwt_required
def delete_products(product_id):
    sql = 'DELETE FROM products WHERE product_id=%s;'
    cursor.execute(sql, [product_id])
    CONNECTION.commit()
    return jsonify({"message":"Successfully deleted product"})

@APP.route('/api/v2/sales', methods=['POST'])
@jwt_required
def create_sales():
    data = request.json.get
    attendant = data('attendant')
    office = data('office')
    price = data('price')
    date = dt.now()
    if not attendant or not office or not price:
        return jsonify({'message': 'Attendant, office and price should not be empty. '}), 400
    if not attendant.isalnum():
        return jsonify({'message': 'attendant contains only alphabets or numbers'}), 400
    sql = 'SELECT * FROM sales WHERE attendant=%s;'
    cursor.execute(sql, ([attendant]))
    existing = cursor.fetchall()
    if not existing:
        sql = 'INSERT INTO sales(attendant, office, price, created_on) VALUES(%s, %s, %s, %s);'
        cursor.execute(sql, (attendant, office, price, date))
        CONNECTION.commit()
        return jsonify({"message":"sale created successfully"}), 201
    return jsonify({"message": "That sale already exists"})    
    

@APP.route('/api/v2/sales/', methods=['GET'])
@jwt_required
def get_sales():
    sql = 'SELECT * FROM sales ORDER BY sale_id;'
    cursor.execute(sql)
    sales = cursor.fetchall()
    return jsonify({"sales": sales})

@APP.route('/api/v2/sales/<int:sale_id>', methods=['GET'])
@jwt_required
def get_sale(sale_id):
    sql = 'SELECT * FROM sales WHERE sale_id=%s;'
    cursor.execute(sql, ([sale_id]))
    sale = cursor.fetchall()
    return jsonify({"sales": sale})

@APP.route('/api/v2/sales/<int:sale_id>', methods=['DELETE'])
@jwt_required
def delete_sales(sale_id):
    sql = 'DELETE FROM sales WHERE sale_id=%s;'
    cursor.execute(sql, [sale_id])
    CONNECTION.commit()
    return jsonify({"message":"Successfully deleted sale"})

@APP.route('/api/v2/sales/<int:sale_id>', methods=['PUT'])
@jwt_required
def edit_sale(sale_id):
    data = request.json.get
    attendant = data('attendant')
    office = data('office')
    price = data('price')
    if not request.json:
        return jsonify({'message': 'Data must be in jsonify'}), 400
    if not attendant or not office or not price:
        return jsonify({'message': 'Attendant, office and price should not be empty.'}), 400
    if not attendant.isalnum():
        return jsonify({'message': 'Attendant contains only alphabets or numbers'}), 400        
    if not office.isalnum():
        return jsonify({'message': 'Office contains alphabets or mixed with nunbers'}), 400
    if not price.isnumeric():
        return jsonify({'message': 'Price contains only numbers'}), 400
    sql = 'UPDATE sales SET attendant=%s, office=%s, price=%s WHERE sale_id=%s;'
    cursor.execute(sql, (attendant, office, price, sale_id))
    CONNECTION.commit()
    return jsonify({"message":"Sale updated successfully"}), 201
