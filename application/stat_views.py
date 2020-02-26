from datetime import date as pydate
from datetime import time as pytime

from flask import redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField

from application import app, db, uploads
from application.domain.log import log
from application.domain.match import match

# this form is only used by stats date picker
class DateForm(FlaskForm):
    start = DateField("start")
    end = DateField("end")

    def validate(self):
        if self.start.data is None and self.end.data is None:
            return True
        elif self.start.data and not self.end.data:
            self.end.errors = list(self.end.errors)
            self.end.errors.append('Please pick a date valid range')
            return False
        elif self.end.data and not self.start.data:
            self.end.errors = list(self.end.errors)
            self.end.errors.append('Please pick a date valid range')
            return False

        if self.start.data > self.end.data:
            self.end.errors = list(self.end.errors)
            self.end.errors.append('Please pick a date valid range')
            return False
        else:
            return True


def get_defaults():
    chars = db.get_chars(current_user.get_id())

    return chars


def generate_view(selected_chars=None, date_range=None, servers=None, my_class=None, other_class=None):
    logs = db.get_logs(current_user.get_id(), chars=selected_chars,
                       date_range=date_range, servers=servers, player_class=my_class)
    log_ids = []
    total = 0
    chars = get_defaults()
    match_ids = []
    for log in logs:
        log_ids.append(log.id)
        for match in log.matches:
            total += 1
            match_ids.append(match.id)
    if log_ids:
        win_precentage = round(db.win_pre(log_ids)*100, 2)
    else:
        win_precentage = 0
    player_counts = db.player_count(match_ids, classes=other_class)
    for player in player_counts:
        if player[3] is not None:
            player[3] = round(player[3]*100, 2)
        else:
            player[3] = " - "
        if player[4] is not None:
            player[4] = round(player[4]*100, 2)
        else:
            player[4] = " - "
    return logs, win_precentage, player_counts, total, chars

@app.route("/stats", methods=["GET", "POST"])
@login_required
def stats():
    if request.method == "G-ET":
        logs, win_precentage, player_counts, total, chars = generate_view()
        return render_template("stats.html", logs=logs, win_pre=win_precentage, players=player_counts, total=total, chars=chars, form=DateForm())
    else:
        form = DateForm(request.form)
        if not form.validate():
            logs, win_precentage, player_counts, total, chars = generate_view()
            return render_template("stats.html", logs=logs, win_pre=win_precentage, players=player_counts, total=total, chars=chars, form=form)

        my_classes = request.form.getlist("my_class_select")
        other_classes = request.form.getlist("enemy_class_select")
        selected_chars = request.form.getlist("char_select")
        servers = request.form.getlist("server_select")
        range = None
        if form.start.data:
            range = [form.start.data, form.end.data]
        logs, win_precentage, player_counts, total, chars = generate_view(
            selected_chars=selected_chars, date_range=range, servers=servers, my_class=my_classes, other_class=other_classes)

        return render_template("stats.html", logs=logs, win_pre=win_precentage, players=player_counts, total=total, chars=chars, form=form)
