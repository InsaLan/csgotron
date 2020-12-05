from aiohttp import web
from .common import client
from ..db import models as db
import json, pytest

async def test_match_create(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()

    db.session.add(db.Server.Server(ip="10.10.10.1", port=8080, nickname="perdu"))
    db.session.add(db.Team.Team(name="Algebre", nationality="France"))
    db.session.add(db.Team.Team(name="Analyse", nationality="France"))
    db.session.commit()

    data = {
        "idTeamA": 1,
        "idTeamB": 2,
        "idServer": 1,
        "map": "de_dust",
        "maxRound": 32,
        "password": "p!k@chu"
    }

    resp = await client.post('/match', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()

    expected = {
      "playAllRound": True,
      "map": "de_dust",
      "streamerReady": False,
      "knifeRound": True,
      "server": {
        "nickname": "perdu",
        "ip": "10.10.10.1",
        "id": 1,
        "port": 8080
      },
      "id": 1,
      "maxRound": 32,
      "teamA": {
        "nationality": "France",
        "name": "Algebre",
        "id": 1
      },
      "overtime": True,
      "teamB": {
        "nationality": "France",
        "name": "Analyse",
        "id": 2
      },
      "autostartMatch": True
    }

    assert received_data == expected
