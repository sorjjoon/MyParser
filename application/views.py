from flask import render_template, request, url_for, redirect, session
from flask_login import login_required, current_user
from application import app, db, uploads
from application.reader import parse_log
from application.domain.match import match
from application.domain.log import log
from datetime import date as pydate
from datetime import time as pytime
from wtforms import SelectMultipleField

from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.html5 import DateField


class DateForm(FlaskForm):
    start = DateField("start")
    end = DateField("end")
    def validate(self):
        if self.start.data is None and self.end.data is None:
            return True
        elif self.start.data and not self.end.data:            
            self.end.errors = list(self.end.errors)
            self.end.errors.append('Please pick a valid range')
            return False
        elif self.end.data and not self.start.data:
            self.end.errors = list(self.end.errors)
            self.end.errors.append('Please pick a valid range')
            return False

        if self.start.data > self.end.data:            
            self.end.errors = list(self.end.errors)
            self.end.errors.append('Please pick a valid range')
            return False
        else:
            return True


def get_defaults():
    chars = db.get_chars(current_user.get_id())
    
    return chars

    
def generate_view(selected_chars = None, date_range=None, servers= None, my_class=None, other_class=None):
    logs = db.get_logs(current_user.get_id(), chars=selected_chars, date_range=date_range, servers=servers, player_class=my_class)        
    log_ids=[]
    total = 0
    chars = get_defaults()
    match_ids=[]
    for log in logs:
        log_ids.append(log.id)
        for match in log.matches:
            total+=1
            match_ids.append(match.id)
    if log_ids: 
        win_prec = round(db.win_pre(log_ids)*100,2)
    else:
        win_prec = 0
    player_counts = db.player_count(match_ids, classes=other_class)
    for player in player_counts:
        if player[3] is not None:
            player[3]=round(player[3]*100,2)
        else:
            player[3] = " - "
        if player[4] is not None:
            player[4]=round(player[4]*100,2)
        else:
            player[4] = " - "
    return logs, win_prec, player_counts, total, chars

@app.route("/")
def index():   
    
    return render_template("index.html")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404
    
@app.route("/show/<log_id>")
@login_required
def show_log(log_id):
    log = db.get_log(log_id, current_user.get_id())
    if not log:
        return redirect(url_for("index"))

    return render_template("view.html", log = log)



@app.route("/delete/<log_id>/", methods=["POST", "GET"])
def delete_log(log_id):
    print("deleting log "+str(log_id))

    db.delete_log(log_id, current_user.get_id())
    return redirect(url_for("logs"))

@app.route("/logs", methods=["GET"])
@login_required
def logs():
    logs = db.get_logs(current_user.get_id())        
    return render_template("list.html", logs = logs)


@app.route("/update/<log_id>", methods=["GET","POST"])
@login_required
def update_log(log_id):
    if request.method =="GET":
        log = db.get_log(log_id, current_user.get_id())
        #TODO fix update_log template placeholder

        session["id"]=log.id
        return render_template("update_log.html", log = log)
    
    log_id = int(session["id"])
    

    date = request.form.get("date")

    log_note = request.form.get(str(log_id)+"log_note")
    print("log note "+ log_note)
    match_ids = db.get_match_ids([log_id])
    matches = []
    errors = False #changed to true if a match fails to validate (for validation see match.py)
    for match_number in match_ids:        
        
        round1=bool(int(request.form.get(str(match_number)+"round1")))
        
        round2=bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3") is None:
            round3=None
        else:
            round3=bool(int(request.form.get(str(match_number)+"round3")))
        
        note = request.form.get(str(match_number)+"note")
        
        new_match = match(request.form.get(str(match_number)+"start"), request.form.get(str(match_number)+"end"), round1, round2, round3, [], [], note=note, id=match_number, team_string=request.form.get(str(match_number)+"team"), opponent_string=request.form.get(str(match_number)+"enemy"))
        if not new_match.validate():
            errors = True
        matches.append(new_match)

    if errors:
        log = db.get_log(log_id,current_user.get_id(),only_details=True).set_matches(matches)
        
        render_template("update_log.html", log = log, date=date)

    session.pop("id")
    db.update_log(log_note, current_user.get_id(),log_id,matches, date)
    return redirect("/logs")

@app.route("/chars/", methods=["GET","POST"])
@login_required
def chars():
    return render_template("chars.html", chars = db.get_chars(current_user.get_id()))


@app.route("/stats", methods =["GET", "POST"])
@login_required
def stats():
    if request.method =="GET":
        logs, win_prec, player_counts, total, chars = generate_view()  
        return render_template("stats.html", logs = logs, win_pre=win_prec, players = player_counts, total=total, chars = chars, form = DateForm())
    else:
        form = DateForm(request.form)
        if not form.validate():
            logs, win_prec, player_counts, total, chars = generate_view()  
            return render_template("stats.html", logs = logs, win_pre=win_prec, players = player_counts, total=total, chars = chars, form = form)
            
        my_classes=request.form.getlist("my_class_select")
        other_classes=request.form.getlist("enemy_class_select")
        selected_chars = request.form.getlist("char_select")
        servers = request.form.getlist("server_select")
        range = None
        if form.start.data:
            range = [form.start.data, form.end.data]        
        logs, win_prec, player_counts, total, chars = generate_view(selected_chars=selected_chars, date_range= range, servers = servers,my_class=my_classes, other_class=other_classes)
        
                
        return render_template("stats.html", logs = logs, win_pre=win_prec, players = player_counts, total=total, chars=chars, form = form)



    