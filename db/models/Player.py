from sqlalchemy import Column, Integer, String, ForeignKey,

from db.Config import Base
class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    idTeam = Column(Integer, ForeignKey('team.id'))

