from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from . import Base
import enum

class MatchState(enum.Enum):
    NOT_STARTED = 1,
    STARTING = 2,
    WARMUP_KNIFE = 3,
    FIRST_SIDE = 4,
    SECOND_SIDE = 5,
    FIRST_SIDE_OT = 6,
    SECOND_SIDE_OT = 7,
    PAUSED = 8,
    ENDED = 9

class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    idTeamFirstSideT  = Column(Integer, ForeignKey('team.id'))
    idTeamFirstSideCT  = Column(Integer, ForeignKey('team.id'))
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
    firstSideT = Column(Integer, nullable=False)
    firstSideCT = Column(Integer, nullable=False)
    secondSideT = Column(Integer, nullable=False)
    secondSideCT = Column(Integer, nullable=False)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    state = Column(Enum(MatchState))
    
    server = relationship("Server", lazy='joined')
    teamFirstSideT = relationship("Team", foreign_keys=[idTeamFirstSideT])
    teamFirstSideCT = relationship("Team", foreign_keys=[idTeamFirstSideCT])

    def __repr__(self):
      return "<Match id={}, team {} vs {}>".format(self.id, self.idTeamFirstSideT, self.idTeamFirstSideCT)
