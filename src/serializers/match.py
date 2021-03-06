from aiohttp import web
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from src.db.models.Match import Match, MatchState
from src.serializers.server import ServerSchema
from src.serializers.team import TeamSchema

class MatchSchema(Schema):
  id = fields.Int()
  map = fields.Str(required=True)

  password = fields.Str(required=True)
  maxRound = fields.Int()
  overtime = fields.Bool(missing=True)
  knifeRound = fields.Bool(missing=True)
  streamerReady = fields.Bool(missing=False)
  playAllRound = fields.Bool(missing=True)
  autostartMatch = fields.Bool(missing=True)
  maxRound = fields.Int()
  state = EnumField(MatchState, missing=MatchState.NOT_STARTED)

  # Only in Requests
  idTeamFirstSideT = fields.Int(required=True, load_only=True)
  idTeamFirstSideCT = fields.Int(required=True, load_only=True)
  idServer = fields.Int(required=True, load_only=True)

  # Only in Responses
  server = fields.Nested(ServerSchema, dump_only=True)
  teamFirstSideT = fields.Nested(TeamSchema, dump_only=True)
  teamFirstSideCT = fields.Nested(TeamSchema, dump_only=True)
  
  @post_load
  def make_match(self, data, **kwargs):
    return Match(**data)
