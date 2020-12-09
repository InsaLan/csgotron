from aiohttp import web
from marshmallow import Schema, fields, post_load
from ..db.models.Match import Match

from .server import ServerSchema
from .team import TeamSchema


class BaseMatch(Schema):
<<<<<<< HEAD

  id = fields.Int(strict=True, dump_only=True)
  map = fields.Str(required=True)

  password = fields.Str(required=True)
  maxRound = fields.Int(strict=True)
=======
  id = fields.Int()
  map = fields.Str(required=True)

  maxRound = fields.Int()
>>>>>>> 682c9c8 ([feat] start ApiUser)

  overtime = fields.Bool(missing=True)
  knifeRound = fields.Bool(missing=True)
  streamerReady = fields.Bool(missing=False)
  playAllRound = fields.Bool(missing=True)
  autostartMatch = fields.Bool(missing=True)

<<<<<<< HEAD
  maxRound = fields.Int(strict=True)

=======
  maxRound = fields.Int()
  
>>>>>>> 682c9c8 ([feat] start ApiUser)
  @post_load
  def make_match(self, data, **kwargs):
    return Match(**data)

# This serialization schema is used to parse POST /match body
# Thus, we allow to fill and show the password field
# and we allow the user to fill the Team IDs
# TODO: this whole approch with two derived classes can be replaced by dump_only and load_only
class MatchRequestSchema(BaseMatch):
<<<<<<< HEAD
=======
  password = fields.Str(required=True)

>>>>>>> 682c9c8 ([feat] start ApiUser)
  idTeamA = fields.Int(required=True)
  idTeamB = fields.Int(required=True)
  idServer = fields.Int(required=True)

class MatchResponseSchema(BaseMatch):
  server = fields.Nested(ServerSchema)
  teamA = fields.Nested(TeamSchema)
  teamB = fields.Nested(TeamSchema)
