from sqlalchemy import Column, Integer, String

from db_base import Base


class DemoModels(Base):
    __tablename__ = 'demo_models'
    __table_args__ = {'extend_existing': True}

    STATE_PREFIX = 'device/online/{}'

    MODE_LIMIT = 1
    MODE_NOT_LIMIT = 2

    id = Column(Integer, primary_key=True, nullable=False, doc='主键')
    uid = Column(Integer, nullable=False, doc='用户id')
    sn = Column(String(15), nullable=False, doc='序列号')
