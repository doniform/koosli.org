
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class RegistrationForm(Form):

    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.email()])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])
