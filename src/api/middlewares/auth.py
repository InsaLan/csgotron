from aiohttp import web
import re
from inspect import isfunction
import jwt
from ...db.Cache import Revokation_list
from ..middlewares.exception import AuthorizationException, RevokedTokenException
def auth_required(func):
    func.isAuth = True
    return func

@web.middleware
async def auth_middleware(request, handler):
    try:
        if isfunction(handler):
            auth_req = hasattr(handler, "isAuth")
        else:
            auth_req = hasattr(getattr(handler, request.method.lower()),"isAuth")
        if auth_req:
            auth = request.headers['Authorization']
            if (token := re.match('^Bearer ([-_.a-zA-Z0-9]*)$', auth)) is not None:
                decoded = jwt.decode(token[1],"VerySeCrEt" ,algorithms='HS256')
                if Revokation_list.redis.get(decoded['username']).decode('utf-8') == token[1]:
                    raise RevokedTokenException

                response = await handler(request)
                return response
            else:
                raise AuthorizationException('No bearer provided')
        else:
            response = await handler(request)
            return response
    except AuthorizationException:
        raise AuthorizationException("No bearer provided")
    except jwt.exceptions.ExpiredSignatureError:
        raise jwt.exceptions.ExpiredSignatureError
    except jwt.exceptions.PyJWTError:
        raise jwt.exceptions.PyJWTError
    except KeyError as e:
        raise AuthorizationException('No authorization header provided')

