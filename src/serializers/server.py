from aiohttp import web
from marshmallow import Schema, fields, post_load

from src.db.models.Server import Server

class ServerSchema(Schema):
  id = fields.Int(dump_only=True)
  ip = fields.IPv4()
  port = fields.Int()
  nickname = fields.Str()

  @post_load
  def make_server(self, data, **kwargs):
    return Server(**data)

