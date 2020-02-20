from flask import Flask
from application.database import data
from flask_uploads import UploadSet, configure_uploads, TEXT
import os
from flask import render_template, request

app = Flask(__name__)



#uploads
uploads = UploadSet("logs", TEXT)
app.config["UPLOADED_LOGS_DEST"] =os.getcwd()+"/uploads"
configure_uploads(app, uploads)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 #limit of 20 mb


#db
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_ECHO"] = True
database = SQLAlchemy(app)
db = data(database.engine)

#inserting admin user (if one exsist, unique constraint fail)
try:
    db.insert_user("admin","admin", role="ADMIN")
except:
    pass


#login
from application.auth import account

app.config["SECRET_KEY"] = os.urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_auth"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):        
    return db.get_user_by_id(user_id)

#views, - imported as views1 because imports cant have the same name (but are never manually used so the name doesn't matter)
from application.auth import views as views1
from application import forms
from application import views

