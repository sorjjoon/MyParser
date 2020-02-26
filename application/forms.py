from datetime import date as pydate
from datetime import time as pytime
# used to generate a session_id, session_id appended to the start of all session variables related to a certain log (allows multiple uploads at the same time for an user)
# session used over hidden inputs , because session can't be modified (most importanlty modifying size could allow user to insert an infinite amount of data at once)
from secrets import token_hex

from flask import redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from flask_uploads import UploadNotAllowed
from flask_wtf import FlaskForm
from wtforms import (FieldList, FileField, FormField, PasswordField,
                     SelectField, StringField, validators)

from application import app, db, uploads
from application.domain.log import log
from application.domain.match import match
from application.reader import parse_log

class UploadForm(FlaskForm):
    log = FileField("log")

    class Meta:
        csrf = False
        
class UpdateChar(FlaskForm):
    server = SelectField(u'Server', choices=[('Star Forge', 'Star Forge'), ('Satele Shan', 'Satele Shan'), (
        'Tulak Hord', 'Tulak Hord'), ('Darth Malgus', 'Darth Malgus'), ('The Leviathan', 'The Leviathan')])
    char_class = SelectField(u"Class", choices=[("Mercenary", "Mercenary"), ("Powertech", "Powertech"), ("Assassin", "Assassin"), (
        "Sorcerer", "Sorcerer"), ("Operative", "Operative"), ("Sniper", "Sniper"), ("Marauder", "Marauder"), ("Juggernaut", "Juggernaut")])

    class Meta:
        csrf = False


@app.route("/update/char", methods=["GET"])
@login_required
def update_char():
    if request.method == "GET" and request.args.get("update") is not None:
        name = db.get_char_name_by_id(request.args.get("update"))
        return render_template("update_char.html", form=UpdateChar(), char_name=name, id=request.args.get("update"))
    else:
        return redirect(url_for("index"))


@app.route("/update/char/<char_id>/", methods=["GET", "POST"])
@login_required
def update_char_info(char_id):
    if request.method == "GET":
        return redirect(url_for("index"))
    form = UpdateChar(request.form)
    db.update_char(char_id, form.char_class.data, form.server.data)
    return redirect(url_for("chars"))




@app.route("/newlog", methods=["POST", "GET"])
@login_required
def add_log():
    if request.method == "GET":
        return redirect(url_for("index"))
    matches = []

    # session popping after validations
    things_to_pop = []  # list of all variables to pop after log is inserted

    # session_id instead of hidden inputs, because session can't be modified (most importanlty modifying size could allow user to insert infinite amount of data at once)
    session_id = request.form.get("session_id")

    size = session[session_id+"log_size"]

    player = session[session_id+"player"]

    things_to_pop.append(session_id+"log_size")
    things_to_pop.append(session_id+"player")

    date = request.form.get("date")
    log_note = request.form.get("note")

    errors = False  # changed to true if one of the inputs fails to validate
    for match_number in range(1, size+1):

        team = session[session_id+"match"+str(match_number)+"_team"]
        opponent = session[session_id+"match"+str(match_number)+"_opponent"]
        things_to_pop.append(session_id+"match"+str(match_number)+"_team")
        things_to_pop.append(session_id+"match"+str(match_number)+"_opponent")

        round1 = bool(int(request.form.get(str(match_number)+"round1")))

        round2 = bool(int(request.form.get(str(match_number)+"round2")))

        if request.form.get(str(match_number)+"round3") is None:
            round3 = None
        else:
            round3 = bool(int(request.form.get(str(match_number)+"round3")))

        start_time = pytime.fromisoformat(
            request.form.get(str(match_number)+"start"))

        end_time = pytime.fromisoformat(
            request.form.get(str(match_number)+"end"))

        note = request.form.get(str(match_number)+"note")

        new_match = match(start_time, end_time, round1, round2,
                          round3, team, opponent, number=match_number, note=note)

        if not new_match.validate():
            errors = True
        matches.append(new_match)

    if not errors:
        for thing in things_to_pop:
            session.pop(thing)

        db.insert_log(current_user.get_id(), matches,
                      date, player, note=log_note)
        return redirect(url_for("index"))
    else:
        return render_template("upload.html", form=UploadForm(), matches=matches, size=len(matches), player=player, date=date, id=session_id, note=note)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_log():
    if request.method == "POST" and "log" in request.files:

        # TODO get a better way to check file extension
        try:
            # saving is temprorary, file is deleted from disk after it's been read
            log_name = uploads.save(request.files["log"])
        except UploadNotAllowed:  # catches wrong file extension and too large a file
            return render_template("upload.html", form=UploadForm(), error="Upload a valid file")
        print(log_name + " - " + "saved to storage")

        matches, player = parse_log(log_name)

        if not matches:
            # non valid text file
            return render_template("upload.html", form=UploadForm(), error="Upload a valid file")

        number = 1

        # session_id to enable multiple uploads at the same time
        session_id = token_hex(4)
        session[session_id+"log_size"] = len(matches)
        session[session_id+"player"] = player
        for match in matches:

            session[session_id+"match" + str(number)+"_team"] = match.team
            session[session_id+"match" + str(number)+"_opponent"] = match.opponent            
            number += 1

        return render_template("upload.html", form=UploadForm(), matches=matches, size=len(matches), player=player, id=session_id)
    else:

        return render_template("upload.html", form=UploadForm())
