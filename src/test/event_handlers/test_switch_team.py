from aiohttp import web
from ..common import client
from src.db import models as db
from src.io.event_handlers.switch_team import *

import json, pytest

async def test_bot_switch_game(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()
    db.session.query(db.Match.Match).delete()
    db.session.query(db.Player.Player).delete()
    
    db.session.add(db.Server.Server(ip="10.10.10.1", port=8080, nickname="perdu"))
    db.session.add(db.Team.Team(name="Algebre", nationality="France"))
    db.session.add(db.Team.Team(name="Analyse", nationality="France"))
    db.session.commit()
  
    match = db.Match.Match(
      idTeamFirstSideT=1,
      idTeamFirstSideCT=2,
      idServer=1,
      map='de_dust',
      mapSelectionMode='xxx',
      password='p!k@chu',
      maxRound=32,
      overtime=True,
      knifeRound=True,
      streamerReady=False,
      playAllRound=True,
      autostartMatch=True,
      firstSideT=0,
      firstSideCT=0,
      secondSideT=0,
      secondSideCT=0,
      state=db.Match.MatchState.STARTING
    )

    db.session.add(match)
    db.session.add(db.Player.Player(username="test", id=1010, isBot=True))
    db.session.commit()

    handler = SwitchTeamEventHandler(10, 'BOT', 'Unassigned', 'TERRORIST')
    handler.handle(match)

    qs = db.session.query(db.Player.Player).filter(db.Player.Player.username == 'test')
    assert qs.count() == 1
    pl = qs.one()
 
    assert pl.idTeam == 1
 
    db.session.query(db.Player.Player).delete()
    db.session.query(db.Match.Match).delete()

    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()

