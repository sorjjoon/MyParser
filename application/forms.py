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
  


#This class is a placeholder until the match in Domain is finishd
class match:
    def __init__(self,number:int, rounds: tuple):
        self.number=number
        self.round1=rounds[0]
        self.round2=rounds[1]
        if len(rounds)==2:
            self.round3=None
        else:
            self.round3=rounds[2]


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

        
        return render_template("upload.html", form = LogForm(), matches = matches)
    else:
        
        return render_template("upload.html", form = LogForm())
    
    