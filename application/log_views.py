from datetime import date as pydate
from datetime import time as pytime

from flask import redirect, render_template, request, session, url_for

from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, validators
from wtforms.fields.html5 import DateField

from application import app, db, uploads
from application.domain.log import log
from application.domain.match import match

@app.route("/show/<log_id>")
@login_required
def show_log(log_id):
    log = db.get_single_log(log_id, current_user.get_id())
    if not log:
        return redirect(url_for("index"))

    return render_template("view.html", log=log)


@app.route("/delete/<log_id>/", methods=["POST", "GET"])
def delete_log(log_id):
    print("deleting log "+str(log_id))

    db.delete_log(log_id, current_user.get_id())
    return redirect(url_for("logs"))


@app.route("/logs", methods=["GET"])
@login_required
def logs():
    logs = db.get_logs(current_user.get_id())
    return render_template("list.html", logs=logs)


@app.route("/update/<log_id>", methods=["GET", "POST"])
@login_required
def update_log(log_id):
    if request.method == "GET":
        log = db.get_single_log(log_id, current_user.get_id())

        return render_template("update_log.html", log=log, id=log.id)

    log_id = request.form.get("id")

    date = request.form.get("date")

    log_note = request.form.get(str(log_id)+"log_note")

    match_ids = db.get_match_ids([log_id])
    matches = []
    # changed to true if a match fails to validate (for validation see match.py in domain)
    errors = False
    for match_number in match_ids:

        round1 = bool(int(request.form.get(str(match_number)+"round1")))

        round2 = bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3") is None:
            round3 = None
        else:
            round3 = bool(int(request.form.get(str(match_number)+"round3")))

        note = request.form.get(str(match_number)+"note")

        new_match = match(request.form.get(str(match_number)+"start"), request.form.get(str(match_number)+"end"), round1, round2, round3, [], [], note=note,
                          id=match_number, team_string=request.form.get(str(match_number)+"team"), opponent_string=request.form.get(str(match_number)+"enemy"))
        if not new_match.validate():
            errors = True
        matches.append(new_match)

    if errors:
        log = db.get_single_log(
            log_id, current_user.get_id(), only_details=True).set_matches(matches)

        return render_template("update_log.html", log=log, date=date)

    db.update_log(log_note, current_user.get_id(), log_id, matches, date)
    return redirect("/logs")