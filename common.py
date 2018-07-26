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

    @wraps(func)
    def wrapper(*args, **kwargs):
        from models import OnlineUser
        token = request.cookies.get('token')
        record = OnlineUser.verify_token(token)
        if record:
            token = OnlineUser.create_record(record.id_)
            return set_token(func(*args, **kwargs), token)
        else:
            return redirect('/login')
    return wrapper
