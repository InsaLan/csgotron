from aiohttp import web
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from ..db.models.Match import Match, MatchState

from .server import ServerSchema
from .team import TeamSchema

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
  idTeamA = fields.Int(required=True, load_only=True)
  idTeamB = fields.Int(required=True, load_only=True)
  idServer = fields.Int(required=True, load_only=True)

  # Only in Responses
  server = fields.Nested(ServerSchema, dump_only=True)
  teamA = fields.Nested(TeamSchema, dump_only=True)
  teamB = fields.Nested(TeamSchema, dump_only=True)
  
  @post_load
  def make_match(self, data, **kwargs):
    return Match(**data)
