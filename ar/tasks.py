from ar.models import Menu, BillOrder
import logging
import hashlib

logger = logging.getLogger('ar')


class CheckData():
    @classmethod
    def menu(cls, data: dict):
        required = ['name']
        optional = ['price', 'desc', 'image', 'details']
        for i in required:
            if i not in data:
                return False
        return True

    @classmethod
    def billorder(cls, data: dict):
        required = ['bill_no', 'name', 'quantity']
        # optional = ['desc', 'image', 'details']

        for i in required:
            if i not in data:
                return False

        return True


def encode_menu_name(name: str):
    m = hashlib.sha1(name.encode('utf-8'))
    name_hash = m.hexdigest()
    return name_hash


def menu_operation(data: dict, method: str):
    method = method.upper()

    logger.debug(f'data {data}')
    if not CheckData.menu(data):
        logger.error('check_menu_data() failed!')
        return
    else:
        # do upsert
        if 'name_hash' not in data:
            data['name_hash'] = encode_menu_name(data['name'])

        mu = Menu()
        q = dict(name_hash=data['name_hash'])

        if method == 'POST':
            mu.upsert(q, data)
            return True
        if method == 'PUT':
            mu.update(q, data)
            return True
        if method == 'GET':
            doc = mu.select(q)
            return doc.to_dict()
        if method == 'DELETE':
            doc = mu.select(q)
            mu.delete(doc)
            return True


def menu_search_op(data: dict):
    pass


def billorder_operation(data: dict, method: str):
    method = method.upper()

    logger.debug(f'data {data}')
    if not CheckData.billorder(data):
        logger.error('check_billorder_data() failed!')
        return
    else:
        # do upsert
        if 'name_hash' not in data:
            data['name_hash'] = encode_menu_name(data['name'])

        bo = BillOrder()
        q = dict(name_hash=data['name_hash'])

        if method == 'POST':
            bo.insert(data)
            return True
        if method == 'PUT':
            bo.update(q, data)
            return True
        if method == 'GET':
            doc = bo.select(q)
            return doc.to_dict()
