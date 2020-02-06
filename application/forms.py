from flask_wtf import FlaskForm
from flask import render_template, request, url_for
from wtforms import validators
from application.reader import parse_log

from application import app, db, uploads

from wtforms import FileField, StringField, PasswordField
from flask_uploads import UploadNotAllowed
from flask_login import login_required




class LogForm(FlaskForm):
    log = FileField("log")
    class Meta:
        csrf = False
  



@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_log():
    if request.method == "POST" and "log" in request.files: 
        print("file upload")
        #TODO get a better way to check file extension
        try:
            log_name = uploads.save(request.files["log"]) #saving is temprorary, file is deleted from disk after it's been read
        except UploadNotAllowed:
            print("invalid upload")
            return render_template("upload.html", form = LogForm(), error = "Upload a valid file")
        print(log_name+ " - "+ "saved to storage")

        matches = parse_log(log_name)
        
        if not matches:
            print("non valid text file")
            return render_template("upload.html", form = LogForm(), error = "Upload a valid file")

        print(matches[0].team)
        print(matches[0].opponent)
        return render_template("upload.html", form = LogForm(), matches = matches, size = len(matches))
    else:
        
        return render_template("upload.html", form = LogForm())
    
    