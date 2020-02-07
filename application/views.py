from flask import render_template, request, url_for, redirect, session
from flask_login import login_required, current_user
from application import app, db, uploads
from application.reader import parse_log
from application.forms import LogForm
from application.domain.domain import match
from datetime import date as pydate
from datetime import time as pytime
from application.database.stats import win_pre, player_count

@app.route("/")
def index():   
    return render_template("index.html")




@app.route("/list", methods=["GET"])
@login_required
def get_matches():
    
    logs = db.get_logs(current_user.get_id())
    
    log_ids=[]
    for log in logs:
        log_ids.append(log.id)
    if log_ids:
        win_prec = round(win_pre(log_ids)*100,2)
    else:
        win_prec = 0
    player_counts = player_count(log_ids)

    return render_template("list.html", logs = logs, win_pre=win_prec, players = player_counts)




@app.route("/newlog", methods=["POST", "GET"])
@login_required
def add_log():
    if request.method == "GET":
        return redirect(url_for("index"))
    matches =[]

    size = session["log_size"]
    session.pop("log_size")
    date = request.form.get("date")
    
    for match_number in range(1,size+1):
        team = session["match"+str(match_number)+"_team"]
        opponent = session["match"+str(match_number)+"_opponent"]
        session.pop("match"+str(match_number)+"_team")
        session.pop("match"+str(match_number)+"_opponent")
        print(team)
        print(opponent)
        round1=bool(int(request.form.get(str(match_number)+"round1")))
        
        round2=bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3") is None:
            round3=None
        else:
            round3=bool(int(request.form.get(str(match_number)+"round3")))
        
        start_time = pytime.fromisoformat(request.form.get(str(match_number)+"start"))
        end_time= pytime.fromisoformat(request.form.get(str(match_number)+"end"))
        matches.append(match(start_time, end_time, round1, round2, round3, team, opponent))

    db.insert_log(current_user.get_id(),matches,date)

    return redirect(url_for("index"))

