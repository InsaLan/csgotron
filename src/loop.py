from aiohttp import web
from src.db import models as db

def setup_aio():
  db.create_schema()
  app = web.Application()

  from src.api import match, server, team
  app.router.add_routes(match.routes)
  app.router.add_routes(server.routes)
  app.router.add_routes(team.routes)
  
  return app

def create_loop():
   db.init_engine("confinebot.db")
   return setup_aio()
