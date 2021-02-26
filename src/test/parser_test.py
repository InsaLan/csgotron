from src.log_parser.parser import LogParser, BadMessageException
import json, pytest

async def test_parse_simple_log():
  p = LogParser()
  p.parse('"Jeff<22><BOT>" switched from team <Unassigned> to <TERRORIST>')

