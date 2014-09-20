# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort, flash, url_for, redirect, request
from flask import current_app as APP
from flask.ext.login import login_required, current_user, login_user, logout_user

from .models import User
from .forms import RegistrationForm
from koosli import db


mod = Blueprint('user', __name__, url_prefix='/user')


@mod.route('/')
@login_required
def index():
    '''The user dashboard where stats can be seen and preferences changed'''

    return render_template('user_dash.html', user=current_user)


@mod.route("/login", methods=["GET", "POST"])
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
    return redirect(request.args.get('next') or '/user')


@mod.route('/register' , methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'GET' or not form.validate():
        return render_template('user_register.html', form=form)

    if User.email_taken(form.email.data):
        flash('This email belongs to a registered user')
        return render_template('user_register.html', form=form)

    user = User(email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('user.login'))


@mod.route('/logout')
def logout():
    logout_user()
    return redirect('/')
