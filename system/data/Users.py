import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    in_test = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    passed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    question_id = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    last_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    type = sqlalchemy.Column(sqlalchemy.String)
