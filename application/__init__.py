from flask import Flask
from application.database import data
from flask_uploads import UploadSet, configure_uploads, TEXT
import os
from flask import render_template, request


app = Flask(__name__)

uploads = UploadSet("logs", TEXT)

app.config["UPLOADED_LOGS_DEST"] =os.getcwd()+"/uploads"

configure_uploads(app, uploads)


db = data.data()
db.create_tables()


from application import views

