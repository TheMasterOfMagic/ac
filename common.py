def set_token(html: str, token: str):
    from flask import make_response
    r = make_response(html)
    r.set_cookie('token', token)
    return r


def eprint(*args, **kwargs):
    from sys import stderr
    kwargs['file'] = stderr
    return print(*args, **kwargs)


def login_required(func):
    from flask import request, redirect
    from functools import wraps
    from models import User

    @wraps(func)
    def wrapper(*args, **kwargs):
        from models import OnlineUser
        token = request.cookies.get('token')
        record = OnlineUser.verify_token(token)
        if record:
            token = OnlineUser.create_record(record.id_)
            if 'user' in func.__code__.co_varnames:
                kwargs['user'] = User.get_by(id_=record.id_)
            return set_token(func(*args, **kwargs), token)
        else:
            return redirect('/login')
    return wrapper
