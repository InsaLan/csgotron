import logging
from aiohttp import web
from aiohttp_middlewares import cors_middleware
import base64
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS
from aiohttp_session import setup, cookie_storage, session_middleware, SimpleCookieStorage
from cryptography.fernet import Fernet
from src.db import models as db
from src.config import ConfigStore, load_config_from_file
from src.api.middlewares import auth_middleware, error_middleware

def setup_aio():
  key = Fernet.generate_key()
  secret_key = base64.urlsafe_b64decode(key)
  db.create_schema()
  app = web.Application(middlewares=[
          error_middleware,
          #session_middleware(SimpleCookieStorage()),
          session_middleware(cookie_storage.EncryptedCookieStorage(secret_key, cookie_name="API_SESSION")),
          cors_middleware(
          origins=["http://localhost:3000"],
          allow_headers=DEFAULT_ALLOW_HEADERS+ ("Access-Control-Allow-Origin",),
          allow_credentials=True),
          auth_middleware,
])

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
