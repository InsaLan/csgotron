#!/usr/bin/python3
from aiohttp import web
from src.loop import create_loop
import logging

# TODO: put the loglevel in the config
logging.basicConfig(level=logging.DEBUG)

app = create_loop()
web.run_app(app)
