from aiohttp import web
from inspect import isfunction
import re, jwt
from aiohttp_session import *

from src.api.middlewares.exception import AuthorizationException
from src.db import models as db
from src.db.models.ApiUser import ApiUser

def auth_required(func):
    func.isAuth = True
    return func

@web.middleware
async def auth_middleware(request, handler):
    try:
        if isfunction(handler):
            auth_req = hasattr(handler, "isAuth")
        else:
            try:
                auth_req = hasattr(getattr(handler, request.method.lower()),"isAuth")
            except AttributeError:
                auth_req = False
        if auth_req:
                db_session = db.DBSession()
                session = await get_session(request)
                user = db_session.query(ApiUser).filter_by(token=session['session_token']).first()
                if user is not None:
                    response = await handler(request)
                    return response
                db_session.commit()
                raise AuthorizationException("Unknown token")
        else:
            response = await handler(request)
            return response
    except AuthorizationException:
        raise AuthorizationException("No bearer provided")
    except KeyError:
        raise AuthorizationException("No token provided")