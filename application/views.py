from flask import render_template, request, url_for
from flask_login import login_required, current_user
from application import app, db, uploads
from application.reader import parse_log
from application.forms import LogForm
from application.database.data import Player, Log, Match, Account


@app.route("/")
def index():
    Account.query.All()    
    return render_template("index.html")




@app.route("/list", methods=["GET"])
@login_required
def get_matches():
    print(current_user.get_id())
    log_ids = db.get_log_ids(current_user.get_id())
    logs=[]
    for tuples in log_ids:
        logs.append(tuples[0])
    
    matches = db.get_matches(logs)
    match_strings=[]
    for match in matches:
        if match[0]==1:
            round1 = "round 1, win"
        else:
            round1= "round 1, loss"
        if match[1]==1:
            round2 = "round 2, win"
        else:
            round2 = "round 2, loss"
        if match[2]==1:
            round3 = "round 3, win"
        elif match[2]==0:
            round3 = "round 3, loss"
        else:
            round3 = "round 3, not played"
        match_strings.append([round1, round2, round3])


    return render_template("list.html", logs = match_strings)




@app.route("/newlog", methods=["POST"])
@login_required
def add_log():
    matches =[]
    #key format is match_number+"round"+round_number (for example 3round2), match_number is irrelevant (just chronoligal order they appeared in log, can be expanded later)
    
    #len(request.form.keys()-1 always divisiable by 3
    size = len(list(request.form.keys()))-1 #-1 because date
    date = request.form.get("date")
    print(date)
    print(type(date))
    print(request.form)
    for match_number in range(1,int(size/3)+1):
        round1=bool(int(request.form.get(str(match_number)+"round1")))
        
        round2=bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3")=="2":
            round3=None
        else:
            round3=bool(int(request.form.get(str(match_number)+"round3")))
        
        matches.append((round1, round2, round3))

    db.insert_log(current_user.get_id(),matches,date)

    return render_template("index.html")

