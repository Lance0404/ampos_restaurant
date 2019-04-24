from ar import db
import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy import func, Index, Column, ForeignKey
from sqlalchemy import Integer, Boolean, Enum, DateTime, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, backref

# from ar import logger
import logging
from ar import mylogging
# failed to make root logger function normally
logger = logging.getLogger('ar')
# logger = logging.getLogger('cc.models')

from sqlalchemy.orm import load_only
from sqlalchemy.exc import IntegrityError, InvalidRequestError, OperationalError, DatabaseError


class Model(db.Model):
    '''
    some common instance function that will be used by all model

    use upsert or update w/ care, they have different behavior

    - upsert, try insert first if failed then update (don't forget about the foreign key!)
    - update, update immediately
    '''

    __abstract__ = True

    def upsert(self, query: dict=None, data: dict=None):
        '''
        inspired by Eric's save() function in MongoEngine Models
        '''
        if not query:
            query = dict(id=self.id)

        # update self attr by data
        if data:
            # 1. edit self
            for k, v in data.items():
                setattr(self, k, v)
            # 2. for insert use
            doc = self.__class__(**data)
        else:
            # 1. for insert use
            doc = self
            # 2. for update use
            data = self.to_dict()

        retry = 0
        while 1:
            try:

                logger.debug(f'start inserting {doc} to {self.__tablename__}')

                if 1:  # beta version
                    ret = self.select(query)
                    if not ret:
                        db.session.add(doc)
                        db.session.commit()
                        ret = self.select(query)
                        if ret and getattr(ret, 'to_dict', None):
                            for k, v in ret.to_dict().items():
                                setattr(self, k, v)
                        logger.debug(f'insert {self.__tablename__} successful')
                    else:
                        self.update(query, data)
                if 0:  # deprecated
                    db.session.add(doc)
                    db.session.commit()
                    ret = self.select(query)
                    if ret and getattr(ret, 'to_dict', None):
                        for k, v in ret.to_dict().items():
                            setattr(self, k, v)
                    logger.debug(f'insert {self.__tablename__} successful')
                break
            except OperationalError as e:
                db.session.rollback()
                retry += 1
                if retry > 5:
                    logger.error(f'{e}: retry {retry}')
                    raise
            except IntegrityError as e:
                logger.error(e)
                db.session.rollback()
                break

    def commit(self, query: dict=None, data: dict=None):
        try:
            db.session.commit()
            if query:
                self = self.select(query)
            logger.debug(f'self {self}')
            logger.debug(f'commit {self.__tablename__} successful')
        except IntegrityError as e:
            logger.warning(e)
            db.session.rollback()
            self.update(query, data)
            # don't raise

    def update(self, query: dict=None, data: dict=None):

        if not query:
            query = dict(id=self.id)

        if not data:
            data = self.to_dict()

        if 'id' in data:
            data.pop('id')

        retry = 0
        while 1:
            try:
                logger.debug(f'data {data}')
                self.__class__.query.filter_by(**query).update(data)
                db.session.commit()
                ret = self.__class__.query.filter_by(**query).first()
                if ret and getattr(ret, 'to_dict', None):
                    for k, v in ret.to_dict().items():
                        setattr(self, k, v)
                    logger.debug(f'update {self.__tablename__} successful')
                else:
                    logger.debug(f'update {self.__tablename__} failed')
                break
            except OperationalError as e:
                logger.error(e)
                db.session.rollback()
                if retry > 5:
                    logger.error(f'{e}: retry {retry}')
                    logger.debug('usually this should not happen')
                    raise
                    # break
                retry += 1

    # @classmethod
    def select(self, query: dict, order_by: 'column name'=None, asc: bool=True, limit: int=None) -> 'a object or list of objects':
        '''
        return a table record object
        '''
        retry = 0
        while 1:
            try:
                if order_by and limit:
                    if asc:
                        docs = self.__class__.query.filter_by(
                            **query).order_by(order_by.asc()).limit(limit).all()
                    else:
                        docs = self.__class__.query.filter_by(
                            **query).order_by(order_by.desc()).limit(limit).all()
                    logger.debug('query many record successful')
                    return docs
                else:
                    doc = self.__class__.query.filter_by(**query).first()
                    if doc:
                        logger.debug(f'doc {doc}')
                        logger.debug('query a record successful')
                        return doc
                    else:
                        logger.warning(
                            f'query {query} on {self.__tablename__} found nothing!')
                        break

            except OperationalError as e:
                retry += 1
                db.session.rollback()
                logger.error(e)
                if retry > 5:
                    logger.error(f'{e}, retry {retry}')
                    raise
            except DatabaseError as e:
                retry += 1
                db.session.rollback()
                logger.error(e)
                if retry > 5:
                    logger.error(f'{e}, retry {retry}')
                    raise

    def delete(self, doc: 'query object'=None):
        logger.debug('start delete')
        if doc:
            logger.debug(f'start deleting {doc}')
            db.session.delete(doc)
        else:
            db.session.delete(self)
        db.session.commit()
        logger.debug('done delete')


class Menu(Model):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    name_hash = Column(String(100), nullable=False, index=True, unique=True)
    desc = Column(String(1000), nullable=True)
    image = Column(Text(), nullable=True)
    price = Column(Integer, nullable=False, index=True)
    details = Column(Text(), nullable=True)
    _mtime = Column(DateTime(
        timezone=False), onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)


class BillOrder(Model):
    __tablename__ = 'bill_order'
    id = Column(Integer, primary_key=True)
    bill_no = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False, index=True, unique=True)
    name_hash = Column(String(100), nullable=False, index=True, unique=True)
    quantity = Column(Integer, nullable=False, index=True)
    # order time
    otime = Column(DateTime(timezone=False),
                   default=datetime.datetime.utcnow)
    _mtime = Column(DateTime(
        timezone=False), onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)