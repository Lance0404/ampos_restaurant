from flask import Blueprint, request, g, jsonify, current_app, abort
from flask_headers import headers
# from flask_cors import cross_origin
from ar import db
import json
from ar.api import errors
import datetime
from sqlalchemy.orm import joinedload, Load, load_only

from ar.tasks import *

# from ar.models import

bp = Blueprint('endpoints', __name__)


@bp.route('/menu', methods=['POST', 'GET', 'DELETE', 'PUT'])
@headers({'Cache-Control': 's-maxage=0, max-age=0'})
def menu():
    '''
    # create
    curl -v -X POST 'http://localhost:8900/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Hawaiian Pizza", "desc": "All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu1.jpg", "price": 300, "details": ["Italian", "Ham", "Pineapple"]}'

    # update
    curl -v -X PUT 'http://localhost:8900/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Hawaiian Pizza", "desc": "All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu1.jpg", "price": 300, "details": ["Italian", "Ham", "Pineapple", "Test"]}'

    # query
    curl -v -X GET 'http://localhost:8900/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Hawaiian Pizza"}'

    '''

    res = {'msg': '', 'status': False}

    data = request.json
    ret = menu_operation(data=data, method=request.method)

    if ret:
        res = {'msg': 'ok', 'status': True}
        if isinstance(ret, dict):
            res.update({'data': ret})

    res.update(res)
    return jsonify(res), 200


@bp.route('/menu/search', methods=['GET'])
@headers({'Cache-Control': 's-maxage=0, max-age=0'})
def menu_search():
    '''
    # on name
    curl -v -X GET 'http://localhost:8900/v1/menu/search?name=Hawaiian'

    # on name w/ lower case
    curl -v -X GET 'http://localhost:8900/v1/menu/search?name=hawaiian'

    # on name and desc
    curl -v -X GET 'http://localhost:8900/v1/menu/search?name=Hawaiian&desc=toppings'

    # on details (text[])
    curl -v -X GET 'http://localhost:8900/v1/menu/search?details=Ham'

    curl -v -X GET 'http://localhost:8900/v1/menu/search?name=Hawaiian&desc=toppings&details=Ham'

    # search all
    curl -v -X GET 'http://localhost:8900/v1/menu/search'

    # w/ limit and page
    curl -v -X GET 'http://localhost:8900/v1/menu/search?limit=1&page=1'
    '''

    res = {'msg': '', 'status': False}

    # data = request.json
    data = {}
    if request.args:  # ImmutableMultiDict
        for k, v in request.args.items():
            data[k] = v

    current_app.logger.debug(f'data {data}')
    # data['offset'] = int(data.get('offset', 0))
    data['page'] = int(data.get('page', 1))
    data['limit'] = int(data.get('limit', 10))
    ret = menu_search_op(data=data)

    if ret:
        res = {'msg': 'ok', 'status': True}
        if isinstance(ret, list):
            res.update({'data': ret})

    res.update(res)
    return jsonify(res), 200


@bp.route('/billorder', methods=['POST', 'GET', 'PUT'])
@headers({'Cache-Control': 's-maxage=0, max-age=0'})
def billorder():
    '''
    curl -v -X POST 'http://localhost:8900/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Hawaiian Pizza", "quantity": 1}'

    '''

    res = {'msg': '', 'status': False}

    data = request.json
    ret = billorder_operation(data=data, method=request.method)

    if ret:
        res = {'msg': 'ok', 'status': True}
        if isinstance(ret, dict):
            res.update({'data': ret})

    res.update(res)
    return jsonify(res), 200


# ------------------ tests -----------------------

@bp.route('/test', methods=['POST', 'GET', 'DELETE', 'PUT'])
@headers({'Cache-Control': 's-maxage=0, max-age=0'})
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

    res = {'msg': 'ok', 'status': True}
    res.update(res)
    return jsonify(res), 200
