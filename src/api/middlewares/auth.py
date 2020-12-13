from aiohttp import web
<<<<<<< HEAD
from inspect import isfunction
def auth_required(func):
    func.isAuth = True
=======
def auth(func):
    func.auth = True
>>>>>>> 682c9c8c09640026f46c9a5adf69f66d9fdb7a19
    return func

@web.middleware
async def auth_middleware(request, handler):
    response = await handler(request)
<<<<<<< HEAD
    if isfunction(handler):
        auth_req = hasattr(handler, "isAuth")
    else:
        auth_req = hasattr(getattr(handler, request.method.lower()),"isAuth")
    if auth_req:
        try:
            auth = request.headers['Authorization']
            return web.json_response({'success': 'Authorization header found'}, status=200)
        except:
            return web.json_response({'error': 'missing authentification header'}, status=401)
    else:
        return response
=======
    if not hasattr(handler, "auth"):
        return response
    return web.json_response({'error':  'not auth'}, status=403)
>>>>>>> 682c9c8c09640026f46c9a5adf69f66d9fdb7a19
