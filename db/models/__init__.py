from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_DB_URI = 'sqlite:///confinebot.db'
engine = create_engine(_DB_URI, echo=True)

Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()

from .ApiUser import ApiUser
from .Demo import Demo
from .Kill import Kill
from .Match import Match
from .Player import Player
from .Round import Round
from .Server import Server
from .Team import Team
from .Weapon import Weapon

Base.metadata.create_all(engine)