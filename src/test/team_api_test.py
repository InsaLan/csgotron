from aiohttp import web
from .common import client
from ..db import models as db
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
