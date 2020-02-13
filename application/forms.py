from flask_wtf import FlaskForm
from flask import render_template, request, url_for, redirect, session
from wtforms import validators

from application import app, db, uploads

from wtforms import FileField, StringField, PasswordField, SelectField, FieldList, FormField
from flask_uploads import UploadNotAllowed
from flask_login import login_required, current_user

from application.reader import parse_log
from application.domain.domain import match, log
 
from datetime import date as pydate
from datetime import time as pytime

class UpdateChar(FlaskForm):
    server = SelectField(u'Server', choices=[('Star Forge', 'Star Forge'), ('Satele Shan', 'Satele Shan'), ('Tulak Hord', 'Tulak Hord'), ('Darth Malgus', 'Darth Malgus'), ('The Leviathan', 'The Leviathan')])
    char_class = SelectField(u"Class", choices=[("Mercenary","Mercenary"),("Powertech","Powertech"),("Assassin","Assassin"),("Sorcerer","Sorcerer"),("Operative","Operative"),("Sniper","Sniper"),("Marauder","Marauder"),("Juggernaut","Juggernaut")])
    class Meta:
        csrf = False

class UploadForm(FlaskForm):
    log = FileField("log")
    
    class Meta:
        csrf = False




@app.route("/update/char", methods=["GET"])
@login_required
def update_char():
    if request.method == "GET" and request.args.get("update") is not None:
        name = db.get_char_name_by_id(request.args.get("update"))
        return render_template("update_char.html", form = UpdateChar(), char_name = name, id = request.args.get("update") )
    else:
        return redirect(url_for("index"))
    
        
@app.route("/update/char/<char_id>/", methods=["GET","POST"])
@login_required
def update_char_info(char_id):
    if request.method == "GET":
        return redirect(url_for("index"))
    form = UpdateChar(request.form)
    db.update_char(char_id, form.char_class.data, form.server.data)
    return redirect(url_for("chars"))
    
    
       

#TODO update forn
#TODO validation
@app.route("/newlog", methods=["POST", "GET"])
@login_required
def add_log():
    if request.method == "GET":
        return redirect(url_for("index"))
    matches =[]

    #session popping after validations
    things_to_pop=[]
    size = session["log_size"]
    

    player = session["player"]

    things_to_pop.append("log_size")
    things_to_pop.append("player")

    date = request.form.get("date")
    print(request.form)
    errors = False #changed to true if one of the inputs fails to validate
    for match_number in range(1,size+1):
        
        team = session["match"+str(match_number)+"_team"]
        opponent = session["match"+str(match_number)+"_opponent"]
        things_to_pop.append("match"+str(match_number)+"_team")
        things_to_pop.append("match"+str(match_number)+"_opponent")
        
        round1=bool(int(request.form.get(str(match_number)+"round1")))
        
        round2=bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3") is None:
            round3=None
        else:
            round3=bool(int(request.form.get(str(match_number)+"round3")))
        
        start_time = pytime.fromisoformat(request.form.get(str(match_number)+"start"))
        end_time= pytime.fromisoformat(request.form.get(str(match_number)+"end"))
        note = request.form.get(str(match_number)+"note")
        new_match = match(start_time, end_time, round1, round2, round3, team, opponent, number=match_number, note=note)
        if not new_match.validate():
            errors = True
        matches.append(new_match)

    if not errors:
        for thing in things_to_pop:
            session.pop(thing)

        db.insert_log(current_user.get_id(),matches,date, player)
        return redirect(url_for("index"))
    else:
        return render_template("upload.html", form = UploadForm(), matches = matches, size = len(matches), player=player)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_log():
    if request.method == "POST" and "log" in request.files: 
        
        #TODO get a better way to check file extension
        try:
            log_name = uploads.save(request.files["log"]) #saving is temprorary, file is deleted from disk after it's been read
        except UploadNotAllowed:  #catches wrong file extension and too large a file            
            return render_template("upload.html", form = UploadForm(), error = "Upload a valid file")
        print(log_name+ " - "+ "saved to storage")

        matches, player = parse_log(log_name)
        
        if not matches:
            #non valid text file
            return render_template("upload.html", form = UploadForm(), error = "Upload a valid file")
        number = 1
        session["log_size"]=len(matches)
        for match in matches:
            match_dict = {}
            session["match"+str(number)+"_team"]=match.team
            session["match"+str(number)+"_opponent"]=match.opponent
            session["player"] = player
            number+=1
        
        
        return render_template("upload.html", form = UploadForm(), matches = matches, size = len(matches), player=player)
    else:
        
        return render_template("upload.html", form = UploadForm())
    
    