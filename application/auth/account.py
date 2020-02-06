from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField


class account:
    def __init__(self,id, name, password):
        self.id=id
        self.name=name
        self.password=password


    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
        
    def __str__(self):
        return str(self.id)+" "+self.name

        

