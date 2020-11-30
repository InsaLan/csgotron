from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import IPAddressType

from . import Base
class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    ip = Column(IPAddressType)
    port = Column(Integer)
    nickname = Column(String)