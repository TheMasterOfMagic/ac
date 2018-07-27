from flask import Blueprint, render_template, flash, redirect, request
from models import File
from common import *

file = Blueprint('file', __name__)


@file.route('/')
@login_required
def get__file(user):
    from models import File
    files = File.query.filter(File.creator_id == user.id_).all()
    return render_template('file.html', username=user.username, files=files)


@file.route('/upload')
@login_required
def get__upload():
    from form import FileForm
    return render_template('file_upload.html', form=FileForm())


@file.route('/upload', methods=['POST'])
@login_required
def post__upload(user):
    try:
        from form import FileForm
        form = FileForm()
        assert form.validate_on_submit(), 'invalid form fields'
        data = form.file.data
        File.upload_file(user, data)
        flash('上传成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('上传失败！'+message)
    return redirect('/file')


@file.route('/remove')
@login_required
def get__remove(user):
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        File.delete_file(user, filename)
        flash('删除成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('删除失败！'+message)
    return redirect('/file')


@file.route('/download')
@login_required
def get__download(user):
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        return File.download_file(user, filename)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！'+message)
        return redirect('/file')
