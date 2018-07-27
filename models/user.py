from sqlalchemy import Column, String, Integer, Binary
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func
from database import db


class User(db.Model):
    __tablename__ = 'users'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(TIMESTAMP, default=func.now())
    username = Column(String(64))
    hash_password = Column(String(128))
    symmetric_key = Column(Binary(16*8), nullable=False)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create_user(cls, username, hash_password):
        from uuid import uuid4
        user = User.get_by(username=username)
        assert user is None, 'email already registered'
        symmetric_key = uuid4().bytes
        user = User(username=username, hash_password=hash_password, symmetric_key=symmetric_key)
        db.session.add(user)
        db.session.commit()
