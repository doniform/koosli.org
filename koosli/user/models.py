# -*- coding: utf-8 -*-

import arrow
from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from koosli import db
from koosli.utils import get_current_time, STRING_LEN


# User role
ADMIN = 0
STAFF = 1
USER = 2
USER_ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}

# User status
INACTIVE = 0
NEW = 1
ACTIVE = 2
USER_STATUS = {
    INACTIVE: 'inactive',
    NEW: 'new',
    ACTIVE: 'active',
}


class UserStats(db.Model):
    '''Keeps track of search statistics and preferences'''

    id = Column(db.Integer, primary_key=True)
    created_time = Column(db.DateTime, default=get_current_time)

    # Preferences
    search_provider = Column(db.String(STRING_LEN), default="")
    beneficiary = Column(db.String(STRING_LEN), default="")
    ad_network = Column(db.String(STRING_LEN), default="")
    advertising_off = Column(db.Boolean, default=False)

    # Statistics
    queries_made = Column(db.Integer, default=0)
    ads_clicked = Column(db.Integer, default=0)
    money_generated = Column(db.Float, default=0.0)




class User(db.Model, UserMixin):

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    created_time = Column(db.DateTime, default=get_current_time)

    # To be used if we need email validation
    activation_key = Column(db.String(STRING_LEN))

    # Status of the user. If not authenticated, set to NEW
    status_code = Column(db.SmallInteger, default=ACTIVE)

    # Contains preferences and aggregated statistics
    user_stats_id = Column(db.Integer, db.ForeignKey("user_stats.id"))
    user_stats = db.relationship("UserStats", uselist=False, backref="user")

    # Admin or User, access string representation through role property
    role_code = Column(db.SmallInteger, default=USER, nullable=False)

    _password = Column('password', db.String(STRING_LEN), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password hashing by exposing password field only.
    password = db.synonym('_password',
        descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email

    #=========================================
    # Property functions
    #=========================================


    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    def is_authenticated(self):
        return self.status_code == ACTIVE

    #=========================================
    # Class methods
    #=========================================

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(User.email == login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    @classmethod
    def email_taken(cls, email):
        return cls.query.filter(User.email == email).count() != 0
