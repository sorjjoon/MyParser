from flask import render_template, request, redirect, url_for, session

from application import db, app
from flask_login import login_user, logout_user, login_required, current_user
from application.auth import account


@app.route("/users", methods=["GET"])
@login_required
# method requires admin privilages
def list_user():
    if current_user.role != "ADMIN":
        print("Unauthorized access by "+current_user.username)
        return redirect(url_for("index"))
    else:
        users = db.list_users()
        return render_template("auth/user_list.html", users=users)
