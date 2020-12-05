#!/usr/bin/python3
from aiohttp import web
from src.loop import create_loop

app = create_loop()
web.run_app(app)
