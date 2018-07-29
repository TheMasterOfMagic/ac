from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])

    def get_hash_password(self):
        from hashlib import sha512
        return sha512(self.password.data.encode()).digest()


class RegisterForm(PasswordForm):
    username = StringField('username', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])


class LoginForm(PasswordForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class FileForm(FlaskForm):
    from flask_wtf.file import FileRequired
    file = FileField('file', validators=[FileRequired()])
