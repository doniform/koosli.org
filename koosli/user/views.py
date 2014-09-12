# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort, flash, url_for, redirect, request
from flask import current_app as APP
from flask.ext.login import login_required, current_user, login_user, logout_user

from .models import User
from koosli import db


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
def index():
    """The user dashboard where stats can be seen and preferences changed"""
    print "user index called"
    if not current_user.is_authenticated():
        abort(403)
    return render_template('user_dash.html', user=current_user)


@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('user_login.html')

    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email).first()

    if registered_user is None:
        flash('This email does not belong to a registered user' , 'error')
        return redirect('/user/login')

    if not registered_user.check_password(password):
        flash('Wrong password or username' , 'error')
        return redirect('/user/login')

    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or '/user')


@user.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('user_register.html')

    user = User(email=request.form['email'] , password=request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect('/user/login')


@user.route('/logout')
def logout():
    logout_user()
    return redirect('/') 