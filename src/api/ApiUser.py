from aiohttp import web
from sqlalchemy.sql import table, column, select
from hashlib import sha256
import jwt

from ..db import models as db
from ..db.models.ApiUser import ApiUser
from ..serializers.ApiUser import ApiUserCreationSchema, ApiUserAuthSchema

routes = web.RouteTableDef()
SECRET_DEBUG = 'ThisIsASeCretK3y'

@routes.post("/login")

async def login(request):
    userForm = ApiUserAuthSchema()
    data = await request.json()
    try:
        session = db.DBSession()
        user = session.query(ApiUser).filter_by(username=data['username']).first()
        if user.password == data['password']:
            return web.json_response({"success": "you're connected"},status=200)
        else:
            return web.json_response({"error": "bad Credentials"}, status=401)
    except:
        session.rollback()
        raise

        
    
    
@routes.view("/user")
class UserApi(web.View):
    creation_request_schema = ApiUserCreationSchema()

    async def get(self):
        try:
            session = db.DBSession()
        except:
            session.rollback()
            raise
        pass
    
    async def post(self):
        data = await self.request.json()
        user = self.creation_request_schema.load(data)
        try:
            session = db.DBSession()
            session.add(user)
            session.commit()
        except:
            session.rollback()
            raise
        return web.json_response({"success": "The user was successfully created"},status=200)
    async def patch(self):
        pass

    async def delete(self):
        pass