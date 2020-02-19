from flask import render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from application import db, app
from wtforms import  StringField, PasswordField, validators, ValidationError

from flask_login import login_user, logout_user, login_required, current_user
from application.auth import account
#forms
def username_free(form, field):
    if not db.check_user(field.data):
        raise ValidationError('Username in use')
class PasswordForm(FlaskForm): #TODO add old password
    password1 = PasswordField("New Password", validators=[validators.DataRequired(message=None),validators.Length(min=5, max=50, message="Password must be between 5 and 50 characters"), validators.EqualTo("password2", message='Passwords must match')])
    password2 = PasswordField("Confirm Password" )  #Only password1 needs to be validated
    class Meta:
        csrf = False
        
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired(message=None),validators.Length(min=5, max=30, message="Username must be between 5 and 30 characters"),username_free])
    password = PasswordField("Password", validators=[validators.DataRequired(message=None), validators.Length(min=5, max=50, message="Password must be between 5 and 50 characters")])  #TODO password strength
    class Meta:
        csrf = False

class LoginForm(FlaskForm):    
    username = StringField("Username", validators=[validators.DataRequired(message=None),validators.Length(min=5, max=30, message="Username must be between 5 and 30 characters")])
    password = PasswordField("Password", validators=[validators.DataRequired(message=None), validators.Length(min=5, max=50, message="Password must be between 5 and 50 characters")])  #TODO password strength
    class Meta:
        csrf = False

@app.route("/auth/delete", methods =["POST", "GET"])
@login_required
def delete_user():
    if request.method == "GET":        
        return redirect(url_for("index"))

    db.delete_user(current_user.get_id())
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def register():
    if request.method =="GET":
        return render_template("auth/register.html", form = RegisterForm())
    form = RegisterForm(request.form)
    if not form.validate(): #form validation checks if username is free
        return render_template("auth/register.html", form = form)
    try:
        db.insert_user(form.username.data, form.password.data)
        return redirect(url_for("index"))
    except ValueError:
        return render_template("auth/register.html", form = RegisterForm(), error = "Username in use")

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
    form = PasswordForm(request.form)    
    if form.validate(): 
        new_pass = request.form.get("password1") #Doesn't matter if we use 1 or 2 (since we have validated them to be same)
        db.update_password(current_user.get_id(), new_pass)
        logout_user()
        return redirect(url_for("index"))
        
    else:
        return render_template("auth/newpass.html", form = form)
             

@app.route("/auth/logout")
@login_required
def logout_auth():
    logout_user()
    return redirect(url_for("index"))

