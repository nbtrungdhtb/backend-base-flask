# -*- coding: utf-8 -*-
"""User route."""

from flask import Blueprint, g, jsonify, request
from flask_cors import cross_origin

from app.extensions import db
from . import google
from .auth_jwt import encode as jwt_encode
from .auth_jwt import revoke_token
from .helper import login_required

blueprint = Blueprint('user', __name__)


@blueprint.route('/', methods=['GET'])
@login_required()
def get_user():
    user = getattr(g, 'current_identity', None)
    if user:
        return jsonify({'success': 1, 'msg': '', 'data': user})
    return jsonify({'success': 0, 'msg': 'user not logged in'})


@blueprint.route('/', methods=['PUT'])
@login_required()
def update_user(**kwargs):
    pass


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required()
def logout():
    revoke_token(g.current_token)
    return jsonify({'success': 1, "msg": "Access token revoked"})


@blueprint.route('/login_google', methods=['POST'])
@cross_origin()
def login_google():
    input_data = request.get_json(silent=True)
    if not input_data:
        return jsonify({'success': 0, 'msg': 'param not enough'})

    code = input_data['code']
    redirect_url = input_data['redirect_url']

    if code == '' or redirect_url == '':
        return jsonify({'success': 0, 'msg': 'param not enough'})

    email = google.verify(code, redirect_url)
    if not email:
        return jsonify({'success': 0, 'msg': 'verify failed'})

    user = db.isvn.staffs.find_one({'email': email, 'status': 1})
    if not user:
        return jsonify({'success': 0, 'msg': 'Email not found'})

    jwt_data = {
        'id': user['_id'],
        'email': user['email']
    }

    token = jwt_encode(jwt_data).decode('utf-8')

    return jsonify({'success': 1, 'msg': 'verify success', 'token': token})
