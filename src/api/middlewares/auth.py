from aiohttp import web
from inspect import isfunction
def auth_required(func):
    func.isAuth = True
    return func

@web.middleware
async def auth_middleware(request, handler):
    response = await handler(request)
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
