from aiohttp import web
from ..db.models.Server import Server
from marshmallow import Schema, fields, post_load


class ServerSchema(Schema):
  id = fields.Int()
  ip = fields.IPv4()
  port = fields.Int()
  nickname = fields.Str()

  @post_load
  def make_server(self, data, **kwargs):
    return Server(**data)

