from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import TIMESTAMP
from database import db
from common import *


class OnlineUser(db.Model):
    __tablename__ = 'online_users'

    id_ = Column(Integer, ForeignKey('users.id_'), primary_key=True, autoincrement=True)
    token = Column(String(32), primary_key=True)
    last_used = Column(TIMESTAMP)

    @classmethod
    def new_available_token(cls):
        from uuid import uuid4
        record_list = cls.query.all()
        token_list = list(record.token for record in record_list)
        while True:
            token = uuid4().hex
            if token not in token_list:
                record = cls.query.filter(cls.token == token).first()
                if record is None:
                    return token

    @classmethod
    def create_record(cls, id_):
        from datetime import datetime
        token = cls.new_available_token()
        record = cls.get_by(id_=id_)
        if record is None:
            record = OnlineUser(id_=id_, token=token)
            record.last_used = datetime.now()
            db.session.add(record)
        else:
            record.token = token
            record.last_used = datetime.now()
        db.session.commit()
        return token

    @classmethod
    def delete_record(cls, id_):
        record = cls.get_by(id_=id_)
        if record:
            db.session.delete(record)
            db.session.commit()

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def verify_token(cls, token):
        from datetime import datetime
        from config import token_expired
        record = cls.get_by(token=token)
        if record is not None:
            last_used = record.last_used
            now = datetime.now()
            delta = now-last_used
            total_seconds = delta.total_seconds()
            eprint(total_seconds)
            if total_seconds < token_expired:
                return record
        return None
