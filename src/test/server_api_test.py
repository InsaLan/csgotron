from aiohttp import web
from .common import client
from ..db import models as db
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
