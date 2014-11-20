from koosli.user.forms import RegistrationForm

from flask import Blueprint, render_template, request


mod = Blueprint('site', __name__)


@mod.route('/beta')
def search_main():
    return render_template('index.html')

@mod.route('/')
def splash():
    form = RegistrationForm(request.form)
    return render_template('splash.html', form=form)

@mod.route('/about')
def about():
    return render_template('about.html')

@mod.route('/beneficiaries')
def beneficiaries():
    return render_template('beneficiaries.html')

@mod.route('/search_providers')
def search_providers():
    return render_template('search_providers.html')

@mod.route('/advertisers')
def advertisers():
    return render_template('advertisers.html')
