def set_token(html: str, token: str):
    from flask import make_response
    r = make_response(html)
    r.set_cookie('token', token)
    return r


def eprint(*args, **kwargs):
    from sys import stderr
    kwargs['file'] = stderr
    return print(*args, **kwargs)
