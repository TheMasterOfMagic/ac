from flask import Blueprint, render_template, flash, redirect
from common import *

file = Blueprint('file', __name__)


@file.route('/')
@login_required
def get__file(user):
    filenames = ['123.txt']
    return render_template('file.html', username=user.username, filenames=filenames)


@file.route('/upload')
@login_required
def get__upload():
    from form import FileForm
    return render_template('file_upload.html', form=FileForm())


@file.route('/upload', methods=['POST'])
@login_required
def post__upload():
    from form import FileForm
    form = FileForm()
    assert form.validate_on_submit(), 'invalid form fields'
    content = form.file.data.read()
    
    flash('上传成功！')
    return redirect('/file')
