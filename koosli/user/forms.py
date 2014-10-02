# -*- coding: utf8 -*-

from wtforms import Form, BooleanField, TextField, PasswordField, validators, ValidationError
from wtforms.fields.html5 import EmailField

from koosli.utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX
from .models import User

class RegistrationForm(Form):
    '''Form for user registration'''

    email = EmailField('Email Address', [
        validators.Length(min=6, max=35, message=u'Eposten er ikke lang nok til å være gyldig.'),
        validators.email(message=u'Eposten må være på denne formen: <bruker>@<domene>.<com/no/org etc.>.')
    ])
    password = PasswordField('Password', [
        # Not required for interest registration
        #validators.Required(),
        validators.Length(max=PASSWORD_LEN_MAX, message=u'Passordet må ha minst 6 tegn.'),
        #validators.EqualTo('confirm', message='Passwords must match')
    ])
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.Required()])

    def validate_email(form, field):
        if User.email_taken(form.email.data):
            raise ValidationError('Denne eposten er allerede registrert.')


class PreferenceForm(Form):
    '''Form for user preferences'''

    beneficiary = TextField('beneficiary') # TODO Add valid beneficiary validators
    search = TextField('search')
    ads = TextField('ads')
    advertising_off = BooleanField('advertising_off', [])
