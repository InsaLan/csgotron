from ..message.parser import MonParser, BadMessageException
import json, pytest

async def test_parse_simple_log():
  p = MonParser()
  p.parse("\"darkgallium<5><STEAM_1:1:64417199><Unassigned>\" disconnected (reason \"Disconnect\")")
