import redis, logging
from aiohttp import web
from src.db import models as db
from src.config import ConfigStore, load_config_from_file
from src.api.middlewares import auth_middleware, error_middleware

redis_database = redis.Redis(host='localhost', port=6379, db=0)

def setup_aio():
  db.create_schema()
  app = web.Application(middlewares=[error_middleware, auth_middleware])
  
  from src.api import match, server, team, ApiUser

  app.on_startup.append(match.rebuild_match_managers)
  app.on_cleanup.append(match.cleanup_matches)

  app.router.add_routes(match.routes)
  app.router.add_routes(server.routes)
  app.router.add_routes(team.routes)
  app.router.add_routes(ApiUser.routes)
  
  app['match_managers'] = {}

  return app

def create_loop():
   ConfigStore.cfg = load_config_from_file()
   logging.basicConfig(level=ConfigStore.cfg.log_level.value)
   
   db.init_engine("confinebot.db")
   return setup_aio()
