from sqlalchemy import Column

from koosli import db
from koosli.utils import get_current_time

class UserQuery(db.Model):

    id = Column(db.Integer, primary_key=True)
    created_time = Column(db.DateTime, default=get_current_time)
    query_string = Column(db.String(), nullable=False)
    location = Column(db.String())

    def __repr__(self):
        return '<Query %r>' % self.id
