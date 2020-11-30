from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from . import Base
class Weapon(Base):
    __tablename__ = 'weapon'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String)