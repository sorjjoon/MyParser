from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from application import app, db
from wtforms import  StringField, PasswordField


class account:
    def __init__(self, name, password):
        self.name=name
        self.password=password

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")  
    class Meta:
        csrf = False


@app.route("/auth/login", methods = ["GET", "POST"])
def login_auth():
    if request.method == "GET":
        return render_template("auth/login.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    
    if not check_user(form.username.data, form.password.data):
        return render_template("auth/login.html", form = form,
                               error = "No such username or password")


    print("User " + form.username.data+ " validated")
    return redirect(url_for("index"))

#TODO make this secure (password in plain)
def check_user(username: str, password: str):
    results = db.get_password(username)
    if not results:
        return False
    # Results shouldn't have multiples...    
    correct_password=results[0]
    if password == correct_password:
        return True
    
    return False

