# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import jwt
from flask import request

from app.extensions import config, db_redis
from app.utils import get_uuid

_jwt_config = {
    'secret': config.get('JWT_SECRET_KEY', ''),
    'algorithm': config.get('JWT_ALGORITHM', 'HS256'),
    'leeway': timedelta(seconds=config.get('JWT_LEEWAY', 10)),
    'verify_claims': config.get('JWT_VERIFY_CLAIMS', ['signature', 'exp', 'nbf', 'iat']),
    'required_claims': config.get('JWT_REQUIRED_CLAIMS', ['exp', 'iat', 'nbf']),
    'expiration_delta': timedelta(seconds=config.get('JWT_EXPIRATION_DELTA', 300)),
    'not_before_delta': timedelta(seconds=config.get('JWT_NOT_BEFORE_DELTA', 0))
}


class JWTError(Exception):
    def __init__(self, error, description, status_code=401, headers=None):
        Exception.__init__(self)
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        return 'JWTError: %s' % self.error

    def __str__(self):
        return '%s. %s' % (self.error, self.description)

    def to_dict(self):
        rv = dict(())
        rv['status_code'] = self.status_code
        rv['error'] = self.error + '. ' + self.description
        rv['data'] = ''
        return rv


def _jwt_payload_callback(identity):
    iat = datetime.utcnow()
    exp = iat + _jwt_config.get('expiration_delta')
    nbf = iat + _jwt_config.get('not_before_delta')
    jti = "{iat}_{uuid}".format(iat=iat, uuid=get_uuid())
    # identity = getattr(identity, 'id') or identity['id']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'jti': jti, 'identity': identity}


def _jwt_headers_callback(identity):
    return None


def request_handle():
    auth_header_value = request.headers.get('Authorization', None)
    auth_body_value = request.values.get('Authorization', None)

    if auth_header_value:
        parts = auth_header_value.split()
    elif auth_body_value:
        parts = auth_body_value.split()
    else:
        return

    auth_header_prefix = ['jwt', 'token', 'bearer']

    if parts[0].lower() not in auth_header_prefix:
        raise JWTError('Invalid JWT header', 'Unsupported authorization type')
    elif len(parts) == 1:
        raise JWTError('Invalid JWT header', 'Token missing')
    elif len(parts) > 2:
        raise JWTError('Invalid JWT header', 'Token contains spaces')

    return parts[0], parts[1]


def decode(token):
    options = {
        'verify_' + claim: True
        for claim in _jwt_config.get('verify_claims')
    }

    options.update({
        'require_' + claim: True
        for claim in _jwt_config.get('required_claims')
    })

    return jwt.decode(token, _jwt_config.get('secret'), options=options, algorithms=[_jwt_config.get('algorithm')],
                      leeway=_jwt_config.get('leeway'))


def encode(identity):
    payload = _jwt_payload_callback(identity)
    missing_claims = list(set(_jwt_config.get('required_claims')) - set(payload.keys()))

    if missing_claims:
        raise RuntimeError('Payload is missing required claims: %s' % ', '.join(missing_claims))

    headers = _jwt_headers_callback(identity)

    return jwt.encode(payload, _jwt_config.get('secret'), algorithm=_jwt_config.get('algorithm'), headers=headers)


def identity(decrypted_token):
    """Dinh danh user"""
    # return userid_table.get(user_id, None)
    return decrypted_token['identity']


def is_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = db_redis.get(jti)
    if entry is None:
        return False
    return entry == 'true'


def revoke_token(decrypted_token):
    jti = decrypted_token['jti']
    exp = decrypted_token['exp']
    db_redis.set(jti, 'true', exp)
