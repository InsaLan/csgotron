from aiohttp import web
from src.db import models as db
from src.api.middlewares import auth_middleware, error_middleware

def setup_aio():
  db.create_schema()
  app = web.Application(middlewares=[error_middleware, auth_middleware])

  from src.api import match, server, team, ApiUser
  app.router.add_routes(match.routes)
  app.router.add_routes(server.routes)
  app.router.add_routes(team.routes)
  app.router.add_routes(ApiUser.routes)
  
  return app

def create_loop():
   db.init_engine("confinebot.db")
   return setup_aio()
