import json, pytest

from src.log_parser.parser import LogParser, BadMessageException
from src.test.common import client

async def test_parse_bot_switch_team(client):
  p = LogParser()
  p.parse('"Jeff<22><BOT>" switched from team <Unassigned> to <TERRORIST>')

async def test_parse_bot_entered_game(client):
  p = LogParser()
  p.parse('"Adrian<14><BOT><>" entered the game')
