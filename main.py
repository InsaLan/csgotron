#!/usr/bin/python3

from aiohttp import web
from src.db import models
from src.api import match

app = web.Application()
app.router.add_routes(match.routes)
web.run_app(app)
