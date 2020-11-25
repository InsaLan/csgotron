from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum

from . import Base
class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    idTeamA  = Column(Integer, ForeignKey('team.id'))
    idTeamB  = Column(Integer, ForeignKey('team.id'))
    idServer = Column(Integer, ForeignKey('server.id'))
    password = Column(String(200), nullable=False)
    map      = Column(String(50), nullable=False)
    mapSelectionMode = Column(String(3), nullable=False)
    maxRound = Column(Integer)
    overtime = Column(Boolean)
    knifeRound = Column(Boolean)
    streamerReady = Column(Boolean)
    playAllRound = Column(Boolean)
    autostartMatch = Column(Boolean)
    firstSideTerrorist = Column(String(1), nullable=False)
    firstSideT = Column(Integer, nullable=False)
    firstSideCT = Column(Integer, nullable=False)
    secondSideT = Column(Integer, nullable=False)
    secondSideCT = Column(Integer, nullable=False)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    state = Column(Enum, nullable=False)