#!/usr/bin/python3

from aiohttp import web
from src.db import models
from src.api import match, server, team

app = web.Application()

app.router.add_routes(match.routes)
app.router.add_routes(server.routes)
app.router.add_routes(team.routes)

web.run_app(app)
