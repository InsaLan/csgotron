from aiohttp import web
import json, pytest

from src.test.common import client
from src.db import models as db
from src.io.event_handlers.round_start import *

async def test_round_start(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()
    db.session.query(db.Match.Match).delete()

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
    db.session.commit()

    handler = RoundStartEventHandler()
    handler.handle(match)

    qs = db.session.query(db.Round.Round).filter(db.Round.Round.matchId == 1, db.Round.Round.id == 1)
    assert qs.count() == 1

    db.session.query(db.Player.Player).delete()
    db.session.query(db.Match.Match).delete()

    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()
