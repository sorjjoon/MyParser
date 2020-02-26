

from flask import Flask
import os
app = Flask(__name__)


# uploads
from flask_uploads import UploadSet, configure_uploads, TEXT

uploads = UploadSet("logs", TEXT)
app.config["UPLOADED_LOGS_DEST"] = os.getcwd()+"/uploads"
configure_uploads(app, uploads)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # limit of 20 mb


# db
from flask_sqlalchemy import SQLAlchemy
from application.database import data

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_ECHO"] = False
database = SQLAlchemy(app)
db = data(database.engine)

# inserting admin user (if one exsist, unique constraint fails)
try:
    db.insert_user("admin", "admin", role="ADMIN")
except:
    pass


# login
from flask_login import LoginManager

app.config["SECRET_KEY"] = os.urandom(32)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_auth"
login_manager.login_message = "Please login to use this functionality."

from application.auth import account


@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)

from application.auth import admin_views
from application import forms
from application import views, stat_views, log_views
from application.auth import views as auth_views, forms as auth_forms
