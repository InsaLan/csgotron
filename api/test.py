from aiohttp import web
from auth import auth, auth_middleware
routes = web.RouteTableDef()

@auth
@routes.get('/test')
async def test(request):
      return web.Response(text="Hello, world")

@routes.get('/not_auth')
async def test2(request):
      return web.Response(text="not authenticated")

app = web.Application(middlewares=[auth_middleware])
app.add_routes(routes)
web.run_app(app,host='127.0.0.1', port=8080)
