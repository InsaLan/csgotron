from aiohttp import web
from .common import client
from ..db import models as db
from ..db.models.Team import Team
import json, pytest

async def test_team_create(client):
    # ensure table is empty before creating Object
    db.session.query(db.Team.Team).delete()
    db.session.commit()

    data = {
        "name": "Algebre",
        "nationality": "France"
    }
    resp = await client.post('/team', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()
    
    data['id'] = 1
    assert data == received_data

async def test_team_list(client):

    data = {
        "id": 1,
        "name": "Algebre",
        "nationality": "France"
    }

    resp = await client.get('/team')
    assert resp.status == 200
    received_data = await resp.json()
    assert received_data == [data]

async def test_team_patch(client):
    # ensure table is empty before creating Object
    db.session.query(db.Team.Team).delete()
    initial_team = Team(name='Analyse', nationality='France')
    db.session.add(initial_team)
    db.session.commit()

    data = {
        "nationality": "Vietnam"
    }
    resp = await client.patch('/team/1', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()
    
    expected_data = {
      "id": 1,
      "name": "Analyse",
      "nationality": "Vietnam"
    }

    assert expected_data == received_data

    # ensure data has been changed accordingly in database
  
    db_obj = db.session.query(db.Team.Team).one()
    assert db_obj.id == 1
    assert db_obj.name == "Analyse"
    assert db_obj.nationality == "Vietnam"


async def test_team_delete(client):
    # ensure table is empty before creating Object
    db.session.query(db.Team.Team).delete()
    initial_team = Team(name='Analyse', nationality='France')
    db.session.add(initial_team)
    db.session.commit()

    resp = await client.delete('/team/1')
    assert resp.status == 204
    
    assert db.session.query(db.Team.Team).count() == 0
