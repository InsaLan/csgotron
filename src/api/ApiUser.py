from aiohttp import web
from sqlalchemy.sql import table, column, select
from hashlib import sha256
import datetime, jwt, re
import secrets
from aiohttp_session import new_session
from src.db import models as db
from src.exceptions import UserDoestNotExists, PasswordDoesNotMatch
from src.db.models.ApiUser import ApiUser
from src.serializers.ApiUser import ApiUserCreationSchema, ApiUserAuthSchema
from src.api.middlewares.auth import auth_required

routes = web.RouteTableDef()


"""
This API endpoint is given an access token to protected route of the api (@auth_required decorator is used to mark a route as "protected")
"""
@routes.post("/login")
async def login(request):
    userForm = ApiUserAuthSchema()
    data = await request.json()
    db_session = db.DBSession()
    try:
        userData = userForm.load(data)
        user = db_session.query(ApiUser).filter_by(username=userData['username']).first()
        if user is None:
            raise UserDoestNotExists
        if user.password != userData['password']:
            raise PasswordDoesNotMatch
        user.token = secrets.token_hex(50) # TODO: enforce this secret
        db_session.commit()
        session =await new_session(request)
        session['session_token'] = user.token
        return web.json_response({'success':'logged'})
    except:
        db_session.rollback()
        raise

        

    
@routes.view("/user")
class UserApi(web.View):
    creation_request_schema = ApiUserCreationSchema()

    @auth_required
    async def get(self):
        return web.json_response({"poke":"ping"})

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
