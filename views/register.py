from flask import Blueprint, render_template, redirect
import re
from form import RegisterForm

register = Blueprint('register', __name__)
username_pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]+')
password_pattern = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,36}')


@register.route('/')
def get__register():
    return render_template('register.html', form=RegisterForm())


@register.route('/', methods=['POST'])
def post__register():
    from models import User
    try:
        form = RegisterForm()
        assert form.validate_on_submit(), 'invalid form fields'
        username = form.username.data
        assert username_pattern.fullmatch(username), 'invalid username'
        password = form.password.data
        confirm_password = form.confirm_password.data
        assert password == confirm_password, 'mismatched password and confirm_password'
        assert password_pattern.fullmatch(password), 'invalid password'
        hash_password = form.get_hash_password()
        User.create_user(username, hash_password)
        return redirect('/login')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        return render_template('register.html', form=RegisterForm(), message=message)
