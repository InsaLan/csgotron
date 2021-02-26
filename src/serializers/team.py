from aiohttp import web
from marshmallow import Schema, fields, post_load

from src.db.models.Team import Team

class TeamSchema(Schema):
  id = fields.Int()
  name = fields.Str()
  nationality = fields.Str()

  @post_load
  def make_team(self, data, **kwargs):
    return Team(**data)

