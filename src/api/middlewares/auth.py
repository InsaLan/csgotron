from aiohttp import web
def auth(func):
    func.auth = True
    return func

@web.middleware
async def auth_middleware(request, handler):
    response = await handler(request)
    if not hasattr(handler, "auth"):
        return response
    return web.json_response({'error':  'not auth'}, status=403)