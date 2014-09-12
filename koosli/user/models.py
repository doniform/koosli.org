# -*- coding: utf-8 -*-

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

    __tablename__ = 'user_stats'

    id = Column(db.Integer, primary_key=True)
    created_time = Column(db.DateTime, default=get_current_time)

    search_provider = Column(db.String(STRING_LEN))
    beneficiary = Column(db.String(STRING_LEN))

    


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    activation_key = Column(db.String(STRING_LEN))
    created_time = Column(db.DateTime, default=get_current_time)


    def __repr__(self):
        return '<User %r>' % self.email

    _password = Column('password', db.String(STRING_LEN), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    
    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    # ================================================================
    role_code = Column(db.SmallInteger, default=USER, nullable=False)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    # ================================================================
    # One-to-many relationship between users and user_statuses.
    status_code = Column(db.SmallInteger, default=INACTIVE)

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    # ================================================================
    # One-to-one (uselist=False) relationship between users and user_stats.
    user_stats_id = Column(db.Integer, db.ForeignKey("user_stats.id"))
    user_stats = db.relationship("UserStats", uselist=False, backref="user")

    # ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(User.email == login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(
                User.email.ilike(keyword),
            )
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    def check_email(self, email):
        return User.query.filter(User.email == email).count() == 0