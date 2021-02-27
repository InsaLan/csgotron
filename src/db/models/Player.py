from sqlalchemy import Column, Boolean, Integer, String, ForeignKey

from . import Base
class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    isBot = Column(Boolean, default=False)
    idTeam = Column(Integer, ForeignKey('team.id'))

    def __repr__(self):
      return "<Player id={}, bot={}, username={}, team={}>".format(self.id, self.isBot, self.username, self.idTeam)
