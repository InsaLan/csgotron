from . import common

from aiohttp import web
from marshmallow import Schema, fields, post_load
from src.db import models as db
from src.db.models.Server import Server
from src.serializers.server import ServerSchema

routes = web.RouteTableDef()

@routes.view("/server")
class ServerApi(web.View):
  schema = ServerSchema()
  
  async def get(self):
    session = db.DBSession()
    qs = session.query(Server).all()
    return web.json_response(self.schema.dump(qs, many=True))

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

@routes.view("/server/{id}")
class ServerDetailsApi(common.DetailsApi):
  schema = ServerSchema()
  
  async def get(self):
    _id = await self.get_object_id()

    session = db.DBSession()
    server = session.query(Server).filter(Server.id == _id).one()
    return web.json_response(self.schema.dump(server))

  async def patch(self):
    _id = await self.get_object_id()
    data = await self.request.json()

    # HACK: exactly the same thing as schema.validate (validate against marshmallow without serializing)
    # but directly raise marshmallow ValidationError instead of returning a dict of validation errors
    self.schema._do_load(data, partial=True, postprocess=False)

    try:
      session = db.DBSession()
      server = session.query(Server).filter(Server.id == _id).one()
      common.patch_object(server, data)

      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.schema.dump(server))

  
  async def delete(self):
    _id = await self.get_object_id()

    try:
      session = db.DBSession()
      server = session.query(Server).filter(Server.id == _id).one()
      session.delete(server)

      session.commit()
    except:
      session.rollback()
      raise

    raise web.HTTPNoContent
