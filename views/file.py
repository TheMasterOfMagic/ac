from flask import Blueprint, render_template, flash, redirect
from common import *

file = Blueprint('file', __name__)


@file.route('/')
@login_required
def get__file(user):
    from models import File
    files = File.query.filter(File.creator_id == user.id_).all()
    filenames = list(f.filename for f in files)
    return render_template('file.html', username=user.username, filenames=filenames)


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
        from models import File
        form = FileForm()
        assert form.validate_on_submit(), 'invalid form fields'
        data = form.file.data
        filename, content_length = data.filename, data.content_length
        assert len(filename) <= 64, 'filename too long (>64B)'
        content = form.file.data.read()
        assert not File.query.filter(File.creator_id == user.id_ and File.filename == filename), 'file already exists'
        assert len(content) < 1*1024*1024, 'file too large (>=10MB)'
        File.upload_file(user, filename, content)
        flash('上传成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('上传失败！'+message)
    return redirect('/file')
