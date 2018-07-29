from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, and_
from os import remove, path, mkdir
import re
from aes import encrypt, decrypt
from database import db
from config import storage_path
import secret

filename_pattern = re.compile(r'[^\u4e00-\u9fa5]+')


class File(db.Model):
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey('users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    hash_value = Column(String(128))
    shared = Column(Boolean, default=False)

    @classmethod
    def upload_file(cls, user, data):
        from hashlib import sha512
        from config import allowed_file_suffix_list
        filename = data.filename
        assert len(filename) <= 64, 'filename too long (>64B)'
        assert filename_pattern.fullmatch(filename), 'no unicode character allowed'
        filename_suffix = filename.rsplit('.', maxsplit=1)[-1]
        assert filename_suffix in allowed_file_suffix_list, 'banned file type'
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert not f, 'file already exists'
        content = data.read()
        assert len(content) < 1*1024*1024, 'file too large (>=10MB)'
        user_id = str(user.id_)+'/'
        if not path.exists(storage_path+user_id):
            if not path.exists(storage_path):
                mkdir(storage_path)
            mkdir(storage_path+user_id)
        # 计算原文件的哈希
        hash_value = sha512(content).hexdigest()
        # 判断文件是否存在
        if not path.exists(storage_path+user_id+hash_value):
            # 加密并存储。加密前得先还原出对称密钥。
            content = encrypt(content, secret.decrypt(user.encrypted_symmetric_key))
            # 同时计算签名
            signature = secret.sign(content)
            # 保存密文与签名
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
            with open(storage_path+user_id+hash_value+'.sig', 'wb') as f:
                f.write(signature)
        creator_id = user.id_
        file = File(creator_id=creator_id, filename=filename, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()

    @classmethod
    def delete_file(cls, user, filename):
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        db.session.delete(f)
        db.session.commit()
        files = File.query.filter(File.hash_value == hash_value).all()
        if not len(files):
            remove(storage_path+str(user.id_)+'/'+hash_value)
            remove(storage_path+str(user.id_)+'/'+hash_value+'.sig')

    @classmethod
    def download_file(cls, user, filename, type_):
        from flask import make_response
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        if type_ == 'hashvalue':
            content = hash_value
            filename = filename + '.hash'
        elif type_ == 'signature':
            # 读取签名
            with open(storage_path+str(user.id_)+'/'+hash_value+'.sig', 'rb') as f_:
                content = f_.read()
                filename = filename+'.sig'
        else:
            # 读取密文
            with open(storage_path+str(user.id_)+'/'+hash_value, 'rb') as f_:
                content = f_.read()
            if type_ == 'plaintext':
                content = decrypt(content, secret.decrypt(user.encrypted_symmetric_key))
            elif type_ == 'encrypted':
                filename = filename + '.encrypted'
        response = make_response(content)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    @classmethod
    def share_file(cls, user, filename):
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        f.shared = not f.shared
        db.session.commit()
