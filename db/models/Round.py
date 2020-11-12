from sqlalchemy import Column, Integer, ForeignKey, Boolean

from db.Config import Base
class Round(Base):
    __tablename__ = 'round'

    roundId = Column(Integer, primary_key=True)
    matchId = Column(Integer, ForeignKey('match.id'), primary_Key=True)
    fkPlayerId = Column(Integer, ForeignKey('player.id'))
    explosed = Column(Boolean)
    defusedPlayerId = Column(Integer, ForeignKey('player.id'))
    plantedPlayerId = Column(Integer, ForeignKey('player.id'))
    winnerTeamId = Column(Integer, ForeignKey('team.id'))