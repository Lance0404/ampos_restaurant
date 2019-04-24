from flask import Blueprint, request, g, jsonify, current_app, abort
from flask_headers import headers
from flask_cors import cross_origin
from ar import db
import json
from ar.api import errors
import datetime
from sqlalchemy.orm import joinedload, Load, load_only

# from ar.models import


bp = Blueprint('endpoints', __name__)

@bp.route('/test', methods=['POST', 'GET', 'DELETE', 'PUT'])
@headers({'Cache-Control': 's-maxage=0, max-age=0'})
@cross_origin()
def test():
    '''
    curl -v -X GET 'http://localhost:8900/v1/test' -H 'Content-Type: application/json'
    '''
    res = {'msg': '', 'status': False}

    if request.method == 'POST':
        current_app.logger.debug(f'test() {request.method}')
    if request.method == 'GET':
        current_app.logger.debug(f'test() {request.method}')
    if request.method == 'DELETE':
        current_app.logger.debug(f'test() {request.method}')
    if request.method == 'PUT':
        current_app.logger.debug(f'test() {request.method}')
    res.update({
        'msg': 'ok',
        'status': True
    })

    return jsonify(res), 200
