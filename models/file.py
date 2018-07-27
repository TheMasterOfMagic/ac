from sqlalchemy import Column, String, Integer, ForeignKey, and_
from os import remove, path, mkdir
import re
from aes import encrypt, decrypt
from database import db
from config import storage_path

filename_pattern = re.compile(r'[^\u4e00-\u9fa5]+')


class File(db.Model):
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey('users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    hash_value = Column(String(128))

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
        creator_id = user.id_
        hash_value = sha512(content).hexdigest()  # 先计算哈希
        print(content)
        content = encrypt(content, user.symmetric_key)  # 再进行加密（换句话说这个哈希值的是原文件的哈希值）
        user_id = str(user.id_)+'/'
        if not path.exists(storage_path+user_id):
            mkdir(storage_path+user_id)
        if not path.exists(storage_path+user_id+hash_value):
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
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

    @classmethod
    def download_file(cls, user, filename):
        from flask import make_response
        print(filename)
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        with open(storage_path+str(user.id_)+'/'+hash_value, 'rb') as f_:
            content = f_.read()
        content = decrypt(content, user.symmetric_key)
        response = make_response(content)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        print(response.headers['Content-Disposition'])
        return response
