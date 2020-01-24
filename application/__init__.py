from flask import Flask
from database import data
#from data import data
app = Flask(__name__)

db = data.data()
db.create_tables()

from application import views
