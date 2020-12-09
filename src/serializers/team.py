from aiohttp import web
from ..db.models.Team import Team
from marshmallow import Schema, fields, post_load

routes = web.RouteTableDef()

class TeamSchema(Schema):
  id = fields.Int(strict=True)
  name = fields.Str()
  nationality = fields.Str()

  @post_load
  def make_team(self, data, **kwargs):
    return Team(**data)

