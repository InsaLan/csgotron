from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = None
session = None
DBSession = None
engine = None

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

def init_engine(filename):
    global Base
    global engine

    engine = create_engine('sqlite:///{}'.format(filename), echo=False)

    # by default sqlite does not enforce FOREIGN KEY constraints,
    # it needs to be activated manually
    event.listen(engine, 'connect', _fk_pragma_on_connect)

    Base = declarative_base() 

def flush_data():
    Base.metadata.drop_all(engine)

def create_schema():
    global Base
    global engine
    global session
    global DBSession

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
