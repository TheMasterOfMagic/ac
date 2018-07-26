from flask import Blueprint, render_template, request, redirect
from common import *

root = Blueprint('root', __name__)


@root.route('')
def index():
    from models import OnlineUser
    token = request.cookies.get('token')
    record = OnlineUser.verify_token(token)
    if record:
        token = OnlineUser.create_record(record.id_)
        return set_token(render_template('index.html'), token)
    else:
        return redirect('/login')
