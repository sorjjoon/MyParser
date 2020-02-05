from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from application import app, db, uploads
from application.reader import parse_log
from application.forms import LogForm
from application.domain.domain import match
from datetime import date as pydate
from datetime import time as pytime

@app.route("/")
def index():    
    return render_template("index.html")




@app.route("/list", methods=["GET"])
@login_required
def get_matches():
    logs = db.get_logs(current_user.get_id())
    for log in logs:
        for match in log.matches:
            print(match.start)    
    return render_template("list.html", logs = logs)




@app.route("/newlog", methods=["POST", "GET"])
@login_required
def add_log():
    if request.method == "GET":
        return redirect(url_for("index"))
    matches =[]
    #key format is match_number+"round"+round_number (for example 3round2), match_number is irrelevant (just chronoligal order they appeared in log, can be expanded later)
    
    #len(request.form.keys() always divisiable by 5
    size = len(list(request.form.keys()))-1 #-1 because date
    date = request.form.get("date")
    print(date)
    print(type(date))
    print(request.form)
    for match_number in range(1,int(size/5)+1):
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

