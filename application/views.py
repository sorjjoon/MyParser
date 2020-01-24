from flask import render_template, request
from application import app, db



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list", methods=["GET"])
def get_matches():
    #TODO make this not shit
    log_ids = db.get_log_ids(1)
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



@app.route("/newlog", methods=["GET"])
def new_log():
    return render_template("new.html")


@app.route("/newlog", methods=["POST"])
def add_log():
    matches =[]
    round3 = int(request.form.get("round3"))
    if(round3==2):
        round3=None
    matches.append((int(request.form.get("round1")),int(request.form.get("round2")),round3))
    db.insert_log(1,matches)
    return render_template("index.html")

