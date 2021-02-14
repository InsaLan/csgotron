from ..message.parser import MonParser, BadMessageException
import json, pytest

async def test_parse_simple_log():
  p = MonParser()
  print(p.parse('"Jeff<22><BOT>" switched from team <Unassigned> to <TERRORIST>'))
  assert False

