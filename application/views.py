from application import app, db
from flask import render_template
from flask_login import current_user, login_required

@app.route("/")
def index():

    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404





@app.route("/chars/", methods=["GET", "POST"])
@login_required
def chars():
    return render_template("chars.html", chars=db.get_chars(current_user.get_id()))


