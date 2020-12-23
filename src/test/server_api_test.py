from aiohttp import web
from .common import client
from ..db import models as db
from ..db.models.Server import Server
import json, pytest

async def test_server_create(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    db.session.commit()

    data = {
        "ip": "10.10.10.1",
        "port": 4242,
        "nickname": "cs1"
    }
    resp = await client.post('/server', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()
    
    data['id'] = 1
    assert data == received_data

async def test_server_list(client):

    data = {
        "id": 1,
        "ip": "10.10.10.1",
        "port": 4242,
        "nickname": "cs1"
    }

    resp = await client.get('/server')
    assert resp.status == 200
    received_data = await resp.json()
    assert received_data == [data]

async def test_server_patch(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    initial_server = Server(ip='10.10.10.1', port=4224, nickname='test')
    db.session.add(initial_server)
    db.session.commit()

    data = {
        "nickname": "csgo"
    }
    resp = await client.patch('/server/1', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()
    
    expected_data = {
      "id": 1,
      "ip": "10.10.10.1",
      "port": 4224,
      "nickname": "csgo"
    }

    assert expected_data == received_data

    # ensure data has been changed accordingly in database
  
    db_obj = db.session.query(db.Server.Server).one()
    assert db_obj.id == 1
    assert db_obj.nickname == "csgo"


async def test_server_delete(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    initial_server = Server(ip='10.10.10.1', port=4224, nickname='test')
    db.session.add(initial_server)
    db.session.commit()

    resp = await client.delete('/server/1')
    assert resp.status == 204
    
    assert db.session.query(db.Server.Server).count() == 0
