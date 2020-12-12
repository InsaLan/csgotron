from aiohttp import web
from ..db.models.Server import Server
from marshmallow import Schema, fields, post_load

routes = web.RouteTableDef()

class ServerSchema(Schema):
  id = fields.Int(dump_only=True)
  ip = fields.IPv4()
  port = fields.Int()
  nickname = fields.Str()

  @post_load
  def make_server(self, data, **kwargs):
    return Server(**data)

