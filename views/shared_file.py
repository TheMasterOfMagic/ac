from flask import Blueprint, render_template, request, flash, redirect

shared_file = Blueprint('shared_file', __name__)


@shared_file.route('/')
def get__():
    from models import File, User
    files = File.query.filter(File.shared).all()
    users = list(User.get_by(id_=file.creator_id) for file in files)
    list_ = list((file.filename, user.username) for file, user in zip(files, users))
    return render_template('shared_file.html', list=list_)


@shared_file.route('/download')
def get__download():
    from models import User, File
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        username = request.args.get('username')
        assert username, 'missing username'
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'signature'), 'unknown type'
        user = User.get_by(username=username)
        return File.download_file(user, filename, type_)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)
        return redirect('/shared_file')
