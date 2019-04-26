from ar.models import Menu, BillOrder
import logging
import hashlib
from ar import db
from .api.errors import *

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
    def menu_search(cls, data: dict):
        # required = ['name']
        optional = ['name', 'desc', 'details', 'offset', 'limit']

        for i in optional:
            if i in data:
                return True
        return False

    @classmethod
    def billorder(cls, data: dict):
        required = ['bill_no', 'name', 'quantity']
        # optional = ['desc', 'image', 'details']

        for i in required:
            if i not in data:
                return False

        return True

    @classmethod
    def lc_datails(cls, data: list):
        '''
        turn all the str in list into lowercase
        '''
        m_data = []
        for i in data:
            m_data.append(i.lower())
        return m_data


def encode_menu_name(name: str):
    m = hashlib.sha1(name.encode('utf-8'))
    name_hash = m.hexdigest()
    return name_hash


def menu_operation(data: dict, method: str):
    method = method.upper()

    logger.debug(f'data {data}')
    if not CheckData.menu(data):
        logger.error('CheckData failed!')
        return
    else:
        # do upsert
        if 'name_hash' not in data:
            data['name_hash'] = encode_menu_name(data['name'])

        mu = Menu()
        q = dict(name_hash=data['name_hash'])

        if 'details' in data:
            tmp = CheckData.lc_datails(data['details'])
        data['details'] = tmp
        logger.debug(f"details {data['details']}")

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


def menu_search_op(data: dict=None):
    '''
    do a sql query with many conditions chained with and

    e.g.
    where [condition 1] and [condition 2]
    '''

    logger.debug(f'data {data}')

    if data and not CheckData.menu_search(data):
        logger.error('CheckData failed!')
    else:
        page = data['page']
        limit = data['limit']
        offset = 0 + limit * (page - 1)
        name_kw = desc_kw = details_kw = None

        q = Menu.query
        if data:
            if 'name' in data:
                name_kw = data['name']
                q = q.filter(Menu.name.ilike(f'%{name_kw}%'))
            if 'desc' in data:
                desc_kw = data['desc']
                q = q.filter(Menu.desc.ilike(f'%{desc_kw}%'))
            if 'details' in data:
                # note: details is text[]
                details_kw = data['details'].lower()
                q = q.filter(Menu.details.contains(f'{{{details_kw}}}'))

        mu_list = q.order_by(Menu.id.asc()).offset(offset).limit(limit).all()
        logger.debug(f'len {len(mu_list)}')
        ret_list = []
        for i in mu_list:
            logger.debug(f'i {i.to_dict()}')
            ret_list.append(i.to_dict())

        return ret_list


def billorder_operation(data: dict, method: str):
    method = method.upper()

    logger.debug(f'data {data}')
    if not CheckData.billorder(data):
        logger.error('CheckData failed!')
        return
    else:
        # do upsert
        if 'name_hash' not in data:
            data['name_hash'] = encode_menu_name(data['name'])

        bo = BillOrder()
        # q = dict(name_hash=data['name_hash'])

        if method == 'POST':
            bo.insert(data)
            return True
        if method == 'GET':
            # doc = bo.select(q, order_by=BillOrder.id)
            q = dict(bill_no=data['bill_no'])
            bo_list = BillOrder.query.filter_by(
                **q).order_by(BillOrder.id.asc()).all()
            ret_list = []
            for i in bo_list:
                ret_list.append(i.to_dict())

            return ret_list


def billorder_stat_op(bill_no: int=None):
    raise QuantityBelowZero # test 

    if bill_no:
        sql_str = f'select aa.bill_no,aa.name,aa.action,aa.quantity,b.price from (select a.bill_no,a.name_hash,a.name,a.action,sum(quantity) as quantity from bill_order as a where a.bill_no = \'{bill_no}\' group by a.bill_no,a.name_hash,a.name,a.action) as aa left join menu as b on aa.name_hash = b.name_hash order by aa.bill_no,aa.name,aa.action'
    else:
        sql_str = f'select aa.bill_no,aa.name,aa.action,aa.quantity,b.price from (select a.bill_no,a.name_hash,a.name,a.action,sum(quantity) as quantity from bill_order as a group by a.bill_no,a.name_hash,a.name,a.action) as aa left join menu as b on aa.name_hash = b.name_hash order by aa.bill_no,aa.name,aa.action'

    # action "add" should come before "remove"

    logger.debug(f'sql_str {sql_str}')
    ret = db.engine.execute(sql_str)
    # logger.debug(f'ret {ret}')

    data = {}
    billno_order = []
    # each (bill_no, name), store the order for later use
    billno_to_name_order = {}  # key=bill_no, val=name[]
    name_map_price = {}
    for row in ret:
        logger.debug(row.items())
        bill_no = row['bill_no']
        name = row['name']
        action = row['action']
        quantity = row['quantity']
        price = row['price']

        name_map_price[name] = price
        # billno_name = (bill_no, name)  # tuple
        # name_price = (name, price)  # tuple

        if bill_no not in billno_order:
            billno_order.append(bill_no)

        billno_to_name_order.setdefault(bill_no, [])
        if name not in billno_to_name_order[bill_no]:
            billno_to_name_order[bill_no].append(name)

        data.setdefault(bill_no, {})
        # data[bill_no].setdefault(name_price, 0)
        data[bill_no].setdefault(name, {})
        data[bill_no][name].setdefault('quantity', 0)

        if action == 'add':
            data[bill_no][name]['quantity'] += quantity
        elif action == 'remove':
            data[bill_no][name]['quantity'] -= quantity

    # calcuate price
    for bill_no, name_lst in billno_to_name_order.items():
        for name in name_lst:
            data[bill_no].setdefault('total_price', 0)
            data[bill_no][name].setdefault('price', 0)
            quantity = data[bill_no][name]['quantity']
            if quantity < 0:
                logger.error(f'quantity {quantity} < 0 should not happen!')
                raise QuantityBelowZero
            name_price = name_map_price[name] * quantity
            data[bill_no][name]['price'] = name_price
            data[bill_no]['total_price'] += name_price

    ret_lst = []
    for bill_no in billno_order:
        tmp = {}
        tmp = {
            'bill_no': bill_no,
            'data': data[bill_no]
        }
        ret_lst.append(tmp)
        # billno_to_name_order[bill_no]

    logger.debug(f'ret_lst {ret_lst}')

    return ret_lst
