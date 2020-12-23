from aiohttp import web
from sqlalchemy.sql import table, column, select
from hashlib import sha256
import datetime
import jwt
import re

from ..db.Cache import Revokation_list
from ..db import models as db
from src.exceptions import UserDoestNotExists, PasswordDoesNotMatch
from ..db.models.ApiUser import ApiUser
from ..serializers.ApiUser import ApiUserCreationSchema, ApiUserAuthSchema
from .middlewares.auth import auth_required
routes = web.RouteTableDef()

SECRET_KEY = "VerySeCrEt" # DEBUG only
JWT_ALGORITHM = "HS256"

"""
This API endpoint is given an access token to protected route of the api (@auth_required decorator is used to mark a route as "protected")
- The token can be revoked TODO
- The token has by default, a revoke time of 2h
"""
@routes.post("/login")
async def login(request):
    userForm = ApiUserAuthSchema()
    data = await request.json()
    session = db.DBSession()
    try:
        userData = userForm.load(data)
        user = session.query(ApiUser).filter_by(username=userData['username']).first()
        if user is None:
            raise UserDoestNotExists
        if user.password != userData['password']:
            raise PasswordDoesNotMatch
        """
        """
        payload = {
            'username': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        session.commit()
        return web.json_response({'token': jwt_token})
    except:
        session.rollback()
        raise

        

@routes.get("/revoke")
@auth_required
async def revoke(request):
    try:
        token_raw = request.headers['Authorization'].split(" ")[1]
        token = jwt.decode(token_raw, SECRET_KEY, algorithms='HS256')
        username = token['username']
        exp = token['exp']
        Revokation_list.redis.set(username, token_raw, exp)
        return web.json_response({"sucess": "The token has been successfully revoked!"})
    except Exception:
        raise Exception

    
    
@routes.view("/user")
class UserApi(web.View):
    creation_request_schema = ApiUserCreationSchema()

    @auth_required
    async def get(self):
        try:
            session = db.DBSession()
            return web.json_response({"sucess": "called from a protected route"})
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
