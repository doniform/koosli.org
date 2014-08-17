from flask import Blueprint, render_template


mod = Blueprint('settings', __name__)


@mod.route('/settings')
def settings_main():
    return render_template('settings_main.html')
