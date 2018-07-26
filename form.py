from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])

    def get_hash_password(self):
        from hashlib import sha512
        return sha512(self.password.data.encode()).hexdigest()


class RegisterForm(PasswordForm):
    username = StringField('username', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])


class LoginForm(PasswordForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
