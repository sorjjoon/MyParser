from flask import render_template, request, url_for, redirect, session
from flask_login import login_required, current_user
from application import app, db, uploads
from application.reader import parse_log
from application.domain.domain import match
from datetime import date as pydate
from datetime import time as pytime
from application.database.stats import win_pre, player_count
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

    
def generate_view(selected_chars = None, date_range=None, servers= None, my_class=None):
    logs = db.get_logs(current_user.get_id(), chars=selected_chars, date_range=date_range, servers=servers, player_class=my_class)        
    log_ids=[]
    total = 0
    chars = get_defaults()
    for log in logs:
        log_ids.append(log.id)
        total+=len(log.matches)
    if log_ids:
        win_prec = round(win_pre(log_ids)*100,2)
    else:
        win_prec = 0
    player_counts = player_count(log_ids)
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


@app.route("/delete/<log_id>/", methods=["POST", "GET"])
def delete_log(log_id):
    if request.method =="GET":
        return redirect(url_for("index"))

    print("deleting log "+str(log_id))

    db.delete_log(log_id, current_user.get_id())
    return redirect(url_for("get_matches"))

@app.route("/list", methods=["GET"])
@login_required
def get_matches():
    logs = db.get_logs(current_user.get_id())        
    return render_template("list.html", logs = logs)




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
        selected_chars = request.form.getlist("char_select")
        servers = request.form.getlist("server_select")
        range = None
        if form.start.data:
            range = [form.start.data, form.end.data]        
        logs, win_prec, player_counts, total, chars = generate_view(selected_chars=selected_chars, date_range= range, servers = servers,my_class=my_classes)
        
                
        return render_template("stats.html", logs = logs, win_pre=win_prec, players = player_counts, total=total, chars=chars, form = form)



    