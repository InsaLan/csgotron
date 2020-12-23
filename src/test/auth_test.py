from aiohttp import web, ClientSession
from .common import client
from ..db import models as db
import json, pytest, jwt 

async def test_apiUser_protected_route(client):
    # empty the database
    session = db.DBSession()
    session.add(db.ApiUser.ApiUser(username="John", password="password"))
    session.commit()

    data = {
        "username": "John",
        "password": "password"
    }
    resp = await client.post('/login', data=json.dumps(data))
    
    assert resp.status == 200
    result_data = await resp.json()

    assert "token" in result_data
