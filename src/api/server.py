from aiohttp import web
from marshmallow import Schema, fields, post_load

from ..db import models as db
from ..db.models.Server import Server
from ..serializers.server import ServerSchema

routes = web.RouteTableDef()

@routes.view("/server")
class ServerApi(web.View):
  schema = ServerSchema()

  async def get(self):
    qs = db.session.query(Server).all()
    return web.json_response(list(map(lambda m: self.schema.dump(m), qs)))

  async def post(self):
    data = await self.request.json()
    server = self.schema.load(data)

    try:
      session = db.DBSession()
      session.add(server)
      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.schema.dump(server))
