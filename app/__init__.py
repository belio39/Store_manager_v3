import os 

from flask import Flask, make_response, jsonify
import psycopg2 as psycopg

APP = Flask(__name__)

CONNECTION = psycopg.connect(\
dbname='store_manager', \
user='denisovich', \
host='localhost', \
password='1990')

from . import views