from datetime import datetime as dt
from flask import abort, jsonify
from werkzeug.security import generate_password_hash


from app import CONNECTION
class DatabaseDriver(object):
  """Class method to create and drop tables"""

  def __init__(self):
    pass


  def create_all(self):

    """create database"""
    users = 'CREATE TABLE IF NOT EXISTS users(\
    id SERIAL PRIMARY KEY, \
    username varchar (32) NOT NULL, \
    email varchar (32) UNIQUE NOT NULL, \
    password VARCHAR (256) NOT NULL, \
    created_on TIMESTAMP NOT NULL,\
    isadmin BOOLEAN default FALSE\
    );'

    products = 'CREATE TABLE IF NOT EXISTS products(\
      product_id SERIAL PRIMARY KEY,\
      name varchar (32) NOT NULL, \
      quantity integer NOT NULL, \
      price money NOT NULL, \
      created_on TIMESTAMP NOT NULL \
    );'

    sales = 'CREATE TABLE IF NOT EXISTS sales(\
      sale_id SERIAL PRIMARY KEY,\
      attendant varchar (32) NOT NULL, \
      office varchar (32) NOT NULL, \
      price money NOT NULL, \
      created_on TIMESTAMP NOT NULL \
    );'

    default_admin = """
      insert into users(username, email, password, created_on, isadmin) Values('Belio', 'rotich@gmail.com', %s, CURRENT_TIMESTAMP, TRUE);
    """
    cursor = CONNECTION.cursor()
    cursor.execute(users)
    cursor.execute(products)
    cursor.execute(sales)
    cursor.execute(default_admin, [generate_password_hash('password'),])
    CONNECTION.commit()
    cursor.close()

  def drop_all(self):
    """Drop Tables"""
    cursor = CONNECTION.cursor()
    cursor.execute('DROP TABLE products;')
    cursor.execute('DROP TABLE users;')
    cursor.close()

class Users():
  """Users objects"""
  def __init__(self, email, username=None, password=None, isadmin=False):
    self.cursor = CONNECTION.cursor()
    self.email = email
    self.username = username
    self.isadmin = isadmin
    self.password = password

  def get_all(self):
    """Get all users from database with emails"""
    sql = 'SELECT * FROM users WHERE email=%s;'
    self.cursor.execute(sql, ([self.email]))
    return self.cursor.fetchall()
  def create_user(self):
    date = dt.now()
    sql = 'INSERT INTO users(username, email, password, created_on) VALUES(%S, %S, %S, %S);'
    #self.password = generate_password_hash(self.password)
    self.cursor.execute(sql, (self.username, self.email, self.password, date))
    CONNECTION.commit()

class Products():
  """Products objects"""
  def __init__(self, product_id, name, quantity, price):
    self.product_id = product_id
    self.date = dt.now()
    self.cursor = CONNECTION.cursor()
    self.name = name
    self.quantity = quantity
    self.price = price
  
  def save(self):
    """Post a product to Database"""
    sql = 'INSERT INT0 products(product, content, posted_on) VALUES (%s, %s, %s, %s);'
    self.cursor.execute(sql, (self.product_id, self.name, self.quantity, self.price, self.date))
    CONNECTION.commit()

  def delete_product(self, product_id):
    """Delete a product"""    
    sql = 'DELETE FROM products WHERE product_id=%s;'
    self.cursor.execute(sql, ([product_id]))
    sql = 'DELETE FROM products WHERE id=%s;'
    self.cursor.execute(sql, ([product_id]))
    CONNECTION.commit()

  def edit_product(self, name, quantity, price):
    """Edit a product"""
    sql = 'UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s;'
    self.cursor.execute(sql, (name, quantity, price))
    CONNECTION.commit()

class Sales():
  def __init__(self, sale_id, attendant, office, price):
    self.sale_id = sale_id
    self.date = dt.now()
    self.cursor = CONNECTION.cursor()
    self.attendant = attendant
    self.office = office
    self.price = price

  def save(self):
    """Post a sale to Database"""
    sql = 'INSERT INT0 sales(sale, content, posted_on) VALUES (%s, %s, %s, %s);'
    self.cursor.execute(sql, (self.sale_id, self.attendant, self.office, self.price, self.date))
    CONNECTION.commit()

  def delete_sale(self, sale_id):
    """Delete a sale"""    
    sql = 'DELETE FROM sale WHERE sale_id=%s;'
    self.cursor.execute(sql, ([sale_id]))
    sql = 'DELETE FROM sales WHERE id=%s;'
    self.cursor.execute(sql, ([sale_id]))
    CONNECTION.commit()

  def edit_sale(self, attendant, office, price):
    """Edit a sale"""
    sql = 'UPDATE sales SET attendant=%s, office=%s, price=%s WHERE id=%s;'
    self.cursor.execute(sql, (attendant, office, price))
    CONNECTION.commit()





  