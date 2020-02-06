from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from application import app, db, uploads
from application.reader import parse_log
from application.forms import LogForm
from application.domain.domain import match
from datetime import date as pydate
from datetime import time as pytime
from application.database.stats import win_pre

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

    return render_template("list.html", logs = logs, win_pre=win_prec)




@app.route("/newlog", methods=["POST", "GET"])
@login_required
def add_log():
    if request.method == "GET":
        return redirect(url_for("index"))
    matches =[]

    size = int(request.form.get("size")) 
    date = request.form.get("date")
    print(size)
    print(request.form) 
    for match_number in range(1,size+1):
        print(match_number)
        round1=bool(int(request.form.get(str(match_number)+"round1")))
        
        round2=bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3") is None:
            round3=None
        else:
            round3=bool(int(request.form.get(str(match_number)+"round3")))

        print(request.form.get(str(match_number)+"start"))
        start_time = pytime.fromisoformat(request.form.get(str(match_number)+"start"))
        end_time= pytime.fromisoformat(request.form.get(str(match_number)+"end"))
        matches.append(match(start_time,end_time,round1, round2, round3, [], []))

    db.insert_log(current_user.get_id(),matches,date)

    return redirect(url_for("index"))

