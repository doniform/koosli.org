# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, abort, flash, url_for, redirect, request
from flask.ext.login import current_user

from koosli.decorators import admin_required
from koosli.search.models import UserQuery
from koosli.user.models import User

mod = Blueprint('admin', __name__, url_prefix='/admin')


@mod.route('/')
@admin_required(current_user)
def index():
    '''The admin dashboard'''

    queries = UserQuery.query.count()
    users = User.query.count()

    return render_template('admin_dash.html',
        user=current_user, query_count=queries, user_count=users)
