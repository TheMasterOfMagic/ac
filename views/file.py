from flask import Blueprint, render_template, redirect
from common import *

file = Blueprint('file', __name__)


@file.route('/')
@login_required
def get__file(user):
    filenames = ['123.txt']
    return render_template('file.html', username=user.username, filenames=filenames)
