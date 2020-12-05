from aiohttp import web
from marshmallow import Schema, fields, post_load
from ..db.models.Match import Match

from .server import ServerSchema
from .team import TeamSchema

routes = web.RouteTableDef()

class BaseMatch(Schema):
  id = fields.Int(strict=True)
  map = fields.Str(required=True)

  maxRound = fields.Int(strict=True)

  overtime = fields.Bool(missing=True)
  knifeRound = fields.Bool(missing=True)
  streamerReady = fields.Bool(missing=False)
  playAllRound = fields.Bool(missing=True)
  autostartMatch = fields.Bool(missing=True)

  maxRound = fields.Int(strict=True)
  
  @post_load
  def make_match(self, data, **kwargs):
    return Match(**data)

# This serialization schema is used to parse POST /match body
# Thus, we allow to fill and show the password field
# and we allow the user to fill the Team IDs
class MatchRequestSchema(BaseMatch):
  password = fields.Str(required=True)

  idTeamA = fields.Int(required=True, strict=True)
  idTeamB = fields.Int(required=True, strict=True)
  idServer = fields.Int(required=True, strict=True)

class MatchResponseSchema(BaseMatch):
  server = fields.Nested(ServerSchema)
  teamA = fields.Nested(TeamSchema)
  teamB = fields.Nested(TeamSchema)
