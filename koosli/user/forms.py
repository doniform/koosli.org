
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.fields.html5 import EmailField

from koosli.utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX

class RegistrationForm(Form):

    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.email()])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=PASSWORD_LEN_MIN, max=PASSWORD_LEN_MAX),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class PreferenceForm(Form):

    beneficiary = TextField('beneficiary') # TODO Add valid beneficiary validators
    search = TextField('search')
    ads = TextField('ads')
    advertising_off = BooleanField()
