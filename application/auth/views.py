from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from application import db, app
from wtforms import  StringField, PasswordField, validators

from flask_login import login_user, logout_user, login_required, current_user
from application.auth import account
#forms
class PasswordForm(FlaskForm):
    #TODO strip whitespace, make validators work, currently EqualTo is not working
    password1 = PasswordField("New Password", validators=[validators.DataRequired(message=None),validators.Length(min=5, max=30, message="Password must be between 5 and 30 chaecters"), validators.EqualTo("password2", message='Passwords must match')])
    password2 = PasswordField("Confirm Password", validators=[validators.DataRequired(message=None), validators.Length(min=5, max=30, message="Password must be between 5 and 30 chaecters")])  #TODO password strength
    class Meta:
        csrf = False

##TODO validate (length)
class LoginForm(FlaskForm):
    #TODO strip whitespace
    username = StringField("Username", validators=[validators.DataRequired(message=None),validators.Length(min=5, max=20, message="Username must be between 5 and 30 characters")])
    password = PasswordField("Password", validators=[validators.DataRequired(message=None), validators.Length(min=5, max=30, message="Password must be between 5 and 30 characters")])  #TODO password strength
    class Meta:
        csrf = False

@app.route("/auth/register", methods = ["GET", "POST"])
def register():
    if request.method =="GET":
        return render_template("auth/register.html", form = LoginForm())
    form = LoginForm(request.form)
    try:
        db.insert_user(form.username.data, form.password.data)
        return redirect(url_for("index"))
    except ValueError:
        return render_template("auth/register.html", form = LoginForm(), error = "Username in use")

@app.route("/auth/login", methods = ["GET", "POST"])
def login_auth():
    if request.method == "GET":
        return render_template("auth/login.html", form = LoginForm())

    
    form = LoginForm(request.form)

    user = db.get_user(form.username.data, form.password.data)
    if user is None:
        return render_template("auth/login.html", form = form, error = "No such username or password")

    login_user(user)

    print("User " + form.username.data+ " validated")
    return redirect(url_for("index"))


@app.route("/user", methods=["GET","POST"])
@login_required
def update_password():
    if request.method == "GET":
        return render_template("auth/newpass.html", form = PasswordForm())
    #EqaulTo validator doesn't seem to work, so checking that passwords are same here
    if request.form.get("password1") == request.form.get("password2") and request.form.get("password1") is not None:     
        new_pass = request.form.get("password1") #Doesn't matter if we use 1 or 2 (since we have validated them to be same)
        db.update_password(current_user.get_id(), new_pass)
        logout_user()
        return redirect(url_for("index"))
        
    return render_template("auth/newpass.html", form = PasswordForm(), error = "Passwords don't match")



    



@app.route("/auth/logout")
@login_required
def logout_auth():
    logout_user()
    return redirect(url_for("index"))
