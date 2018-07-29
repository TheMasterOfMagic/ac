from sqlalchemy import Column, String, Integer, Binary
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func
from database import db


class User(db.Model):
    __tablename__ = 'users'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(TIMESTAMP, default=func.now())
    username = Column(String(64), unique=True)
    hash_password = Column(Binary(64))
    encrypted_symmetric_key = Column(Binary(32), nullable=False)
    encrypted_private_key = Column(Binary(32), nullable=False)
    encrypted_public_key = Column(Binary(32), nullable=False)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create_user(cls, username, hash_password):
        import secret
        user = User.get_by(username=username)
        assert user is None, 'email already registered'
        # 先随机生成一个用户的对称密钥与公私钥
        symmetric_key = secret.new_symmetric_key()
        private_key, public_key = secret.new_pair()
        # 再用服务器的公钥加密这些密钥
        user = User(username=username, hash_password=hash_password,
                    encrypted_symmetric_key=secret.encrypt(symmetric_key),
                    encrypted_private_key=secret.encrypt(private_key),
                    encrypted_public_key=secret.encrypt(public_key)
                    )
        db.session.add(user)
        db.session.commit()
