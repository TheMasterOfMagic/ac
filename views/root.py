from flask import Blueprint, render_template, make_response
from common import *

root = Blueprint('root', __name__)


@root.route('')
@login_required
def index():
    return render_template('index.html')


@root.route('public_key')
def public_key():
    from secret import get_pk_raw
    response = make_response(get_pk_raw())
    response.headers['Content-Disposition'] = 'attachment; filename=public_key'
    return response
