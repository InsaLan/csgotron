from sqlalchemy import Column, Integer, ForeignKey, Boolean

from sqlalchemy_utils import URLType
from . import Base

class Demo(Base):
    __tablename__ = 'demo'

    matchId = Column(Integer, ForeignKey('match.id'), primary_key=True)
    available = Column(Boolean, default=False)
    url = Column(URLType)
    size = Column(Integer)

