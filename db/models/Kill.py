from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy_utils import JSONType #See doc https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.json

from db.Config import Base

class Kill(Base):
    __tablename__ = 'kill'

    killId = Column(Integer, primary_key=True)
    killPosition = Column(JSONType, nullable=False) # Stored as {'x': x, 'y': y, 'z': z} for a more consistant API
    KillerPosition = Column(JSONType, nullable=False)
    weapon = Column(String(255))#TODO: We should maybe switch to Enum type with dynamic configuration loading https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
    KilledId = Column(Integer, ForeignKey('player.id'))
    KillerId = Column(Integer, ForeignKey('player.id'))
    isHeadShot = Column(Boolean)