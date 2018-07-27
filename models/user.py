from sqlalchemy import Column, String, Integer, Binary
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func
from database import db


class User(db.Model):
    __tablename__ = 'users'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(TIMESTAMP, default=func.now())
    username = Column(String(64), unique=True)
    hash_password = Column(String(128))
    encrypted_symmetric_key = Column(Binary(2048), nullable=False)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create_user(cls, username, hash_password):
        from uuid import uuid4
        from rsa import RSAPrivateKey
        user = User.get_by(username=username)
        assert user is None, 'email already registered'
        # 先随机生成一个对称密钥
        symmetric_key = uuid4().bytes
        # 再用服务器的私钥加密该对称密钥
        encrypted_symmetric_key = RSAPrivateKey().load('config/key.pem').export().encrypt(symmetric_key)
        user = User(username=username, hash_password=hash_password, encrypted_symmetric_key=encrypted_symmetric_key)
        db.session.add(user)
        db.session.commit()
