from ar.models import Menu, BillOrder
import logging
import hashlib
from ar import db

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
                details_kw = data['details']
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
        if method == 'PUT':
            logger.error(f'not sure how to do update on this table!')
            return False
            # bo.update(q, data)
            # return True
        if method == 'GET':
            # doc = bo.select(q, order_by=BillOrder.id)
            q = dict(bill_no=data['bill_no'])
            bo_list = BillOrder.query.filter_by(
                **q).order_by(BillOrder.id.asc()).all()
            ret_list = []
            for i in bo_list:
                ret_list.append(i.to_dict())

            return ret_list


def billorder_stat_op(data: dict):

    bill_no = data['bill_no']

    sql_str = f'select a.*,b.price from bill_order as a left join menu as b on a.name_hash = b.name_hash where a.bill_no = \'{bill_no}\';'
    logger.debug(f'sql_str {sql_str}')

    ret = db.engine.execute(sql_str)

    logger.debug(f'ret {ret}')

    for row in ret:

        logger.debug(row)
