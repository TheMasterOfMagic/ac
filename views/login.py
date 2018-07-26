from flask import Blueprint, render_template, redirect
from form import LoginForm
from common import *

login = Blueprint('login', __name__)


@login.route('/')
def get__login():
    return render_template('login.html', form=LoginForm())


@login.route('/', methods=['POST'])
def post__login():
    from models import User, OnlineUser
    try:
        form = LoginForm()
        assert form.validate_on_submit(), 'invalid form fields'
        hash_password = form.get_hash_password()
        username = form.username.data
        user = User.get_by(username=username, hash_password=hash_password)
        assert user, 'incorrect username or password'
        token = OnlineUser.create_record(user.id_)
        return set_token(redirect('/'), token)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        return render_template('login.html', form=LoginForm(), message=message)
