# -*- coding: utf-8 -*-
from functools import wraps

import jwt
from flask import g

from . import auth_jwt as _jwt


def login_required(realm=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth_type, token = _jwt.request_handle()

            if auth_type is None:
                raise _jwt.JWTError('Authorization Required', 'Request does not contain an access type',
                                    headers={'WWW-Authenticate': 'JWT realm="%s"' % realm})

            if token is None:
                raise _jwt.JWTError('Authorization Required', 'Request does not contain an access token',
                                    headers={'WWW-Authenticate': 'JWT realm="%s"' % realm})

            try:
                payload = _jwt.decode(token)
            except jwt.InvalidTokenError as e:
                raise _jwt.JWTError('Invalid token', str(e))

            g.current_identity = identity = _jwt.identity(payload)
            g.current_token = payload['jti']

            if identity is None:
                raise _jwt.JWTError('Invalid JWT', 'User does not exist')

            if _jwt.is_blacklist(payload):
                raise _jwt.JWTError('Invalid JWT', 'Token has been revoked')

            return fn(*args, **kwargs)

        return decorator

    return wrapper
