from sqlalchemy import Column, String, Integer, ForeignKey
from database import db


class File(db.Model):
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey('users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    length = Column(Integer, primary_key=True)
    hash_value = Column(String(128))

    @classmethod
    def upload_file(cls, user, filename, content):
        from config import storage_path
        from hashlib import sha512
        creator_id = user.id_
        length = len(content)
        hash_value = sha512(content).hexdigest()
        with open(storage_path+'hash_value', 'wb') as f:
            f.write(content)
        file = File(creator_id=creator_id, filename=filename, length=length, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()
