from flask_wtf import FlaskForm
from flask import render_template, request, url_for, session
from wtforms import validators
from application.reader import parse_log

from application import app, db, uploads

from wtforms import FileField, StringField, PasswordField
from flask_uploads import UploadNotAllowed
from flask_login import login_required




class UploadForm(FlaskForm):
    log = FileField("log")
    class Meta:
        csrf = False


#TODO update forn

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_log():
    if request.method == "POST" and "log" in request.files: 
        print("file upload")
        #TODO get a better way to check file extension
        try:
            log_name = uploads.save(request.files["log"]) #saving is temprorary, file is deleted from disk after it's been read
        except UploadNotAllowed:  #catches wrong file extension and too large a file
            print("invalid upload")
            return render_template("upload.html", form = UploadForm(), error = "Upload a valid file")
        print(log_name+ " - "+ "saved to storage")

        matches = parse_log(log_name)
        
        if not matches:
            print("non valid text file")
            return render_template("upload.html", form = UploadForm(), error = "Upload a valid file")
        number = 1
        session["log_size"]=len(matches)
        for match in matches:
            session["match"+str(number)+"_team"]=match.team
            session["match"+str(number)+"_opponent"]=match.opponent
            number+=1
        return render_template("upload.html", form = UploadForm(), matches = matches, size = len(matches))
    else:
        
        return render_template("upload.html", form = UploadForm())
    
    