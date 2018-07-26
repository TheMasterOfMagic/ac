from flask import Blueprint, render_template, redirect, request

logout = Blueprint('logout', __name__)


@logout.route('/')
def get__logout():
    from models import OnlineUser
    token = request.cookies.get('token')
    record = OnlineUser.verify_token(token)
    if record:
        OnlineUser.delete_record(record.id_)
        return render_template('logout.html')
    else:
        return redirect('/login')
