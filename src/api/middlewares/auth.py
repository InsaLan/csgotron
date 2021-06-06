from aiohttp import web
from inspect import isfunction
import re, jwt
from aiohttp_session import *
from src.api.middlewares.exception import AuthorizationException, RevokedTokenException

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
                session = await get_session(request)
                print(session['session_token'])
                 
                response = await handler(request)
                return response
        else:
            response = await handler(request)
            return response
    except AuthorizationException:
        raise AuthorizationException("No bearer provided")
    except KeyError:
        raise AuthorizationException("No token provided")