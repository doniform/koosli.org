# -*- coding: utf-8 -*-

from functools import update_wrapper

from flask import g, request, redirect, url_for, current_app, abort



def admin_required(user):
    '''Ensure that the currently logged in user is an admin.
    If user is not logged in, redirect to login page.
    '''

    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            if not user.is_authenticated():
                return redirect(url_for('user.login'))
            elif not user.is_admin():
                abort(403)
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_function, fn)
    return decorator
