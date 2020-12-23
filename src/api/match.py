from aiohttp import web
from marshmallow import Schema, fields, post_load

from . import common
from ..db import models as db
from ..db.models.Match import Match
from ..serializers.match import MatchSchema
from ..io.match_manager import MatchManager

from .middlewares.auth import auth_required 
routes = web.RouteTableDef()


@routes.view("/match")
class MatchApi(web.View):
  schema = MatchSchema()

  async def get(self):
    session = db.DBSession()
    qs = session.query(Match).all()
    return web.json_response(self.schema.dump(qs, many=True))

  async def post(self):
    data = await self.request.json()
    match = self.schema.load(data)
    #match.state = MatchState.started
    match.firstSideT = 0
    match.firstSideCT = 0
    match.secondSideT = 0
    match.secondSideCT = 0
    match.firstSideTerrorist = 'A'
    match.mapSelectionMode = 'rng'

    try:
      session = db.DBSession()
      session.add(match)
      
      session.commit()    
    except:
      session.rollback()
      raise

    manager = MatchManager(match.id)
    await manager.setup()                                     
                                                     
    self.request.app['match_managers'][match.id] = manager


    return web.json_response(self.schema.dump(match))

@routes.view("/match/{id}")
class MatchDetailsApi(common.DetailsApi):
  schema = MatchSchema()
  
  async def get(self):
    _id = await self.get_object_id()

    session = db.DBSession()
    match = session.query(Match).filter(Match.id == _id).one()
    return web.json_response(self.schema.dump(match))

  async def patch(self):
    _id = await self.get_object_id()
    data = await self.request.json()

    # HACK: exactly the same thing as schema.validate (validate against marshmallow without serializing)
    # but directly raise marshmallow ValidationError instead of returning a dict of validation errors
    self.schema._do_load(data, partial=True, postprocess=False)

    try:
      session = db.DBSession()
      match = session.query(Match).filter(Match.id == _id).one()
      common.patch_object(match, data)

      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.schema.dump(match))

  
  async def delete(self):
    _id = await self.get_object_id()

    try:
      session = db.DBSession()
      match = session.query(Match).filter(Match.id == _id).one()
      session.delete(match)

      session.commit()
    except:
      session.rollback()
      raise

    raise web.HTTPNoContent
