# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort, flash, url_for, redirect, request
from flask import current_app as APP
from flask.ext.login import login_required, current_user, login_user

from .models import User
from koosli import db


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    return render_template('user_dash.html', user=current_user)


@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('user_login.html')

    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email, password=password).first()

    if registered_user is None:
        flash('Email or Password is invalid' , 'error')
        return redirect('/user/login')

    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@user.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('user_register.html')

    user = User(request.form['email'] , request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect('/user/login')


@user.route('/logout')
def logout():
    logout_user()
    return redirect('/') 