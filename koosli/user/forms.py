
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.fields.html5 import EmailField

from koosli.utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX

class RegistrationForm(Form):
    '''Form for user registration'''

    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.email()])
    password = PasswordField('Password', [
        #validators.Required(),
        validators.Length(max=PASSWORD_LEN_MAX),
        #validators.EqualTo('confirm', message='Passwords must match')
    ])
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class PreferenceForm(Form):
    '''Form for user preferences'''

    beneficiary = TextField('beneficiary') # TODO Add valid beneficiary validators
    search = TextField('search')
    ads = TextField('ads')
    advertising_off = BooleanField('advertising_off', [])
