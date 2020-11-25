from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Interval
from sqlalchemy_utils import JSONType #See doc https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.json

from . import Base

class Kill(Base):
    __tablename__ = 'kill'

    killId = Column(Integer, primary_key=True)
    killPosition = Column(JSONType, nullable=False) # Stored as {'x': x, 'y': y, 'z': z} for a more consistant API
    killerPosition = Column(JSONType, nullable=False)
    weaponId = Column(Integer, ForeignKey('weapon.id'))
    killedId = Column(Integer, ForeignKey('player.id'))
    killerId = Column(Integer, ForeignKey('player.id'))
    isHeadShot = Column(Boolean)
