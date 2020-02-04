from flask_wtf import FlaskForm
from flask import render_template, request, url_for
from wtforms import validators
from application.reader import parse_log

from application import app, uploads

from wtforms import FileField, StringField, PasswordField
from flask_uploads import UploadNotAllowed
from flask_login import login_required



def type_check(form, field):
    print(field.data)
    if len(field.data) > 50:
        raise ValidationError('Upload a valid log file')


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
            log_name = uploads.save(request.files["log"])
        except UploadNotAllowed:
            print("invalid upload")
            return render_template("upload.html", form = LogForm(), error = "Upload a valid file")
        print(log_name+ " - "+ "saved to storage")

        raw_matches = parse_log(log_name)
        
        if not raw_matches:
            print("non valid text file")
            return render_template("upload.html", form = LogForm(), error = "Upload a valid file")

        matches=[]
        x=1
        print(raw_matches)
        for i in raw_matches:
            matches.append(match(x,i))
            x+=1
        return render_template("upload.html", form = LogForm(), matches = matches)
                    
    else:
        
        return render_template("upload.html", form = LogForm())
    
    