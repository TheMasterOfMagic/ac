from flask import Blueprint, render_template
from common import *

root = Blueprint('root', __name__)


@root.route('')
@login_required
def index():
    return render_template('index.html')
