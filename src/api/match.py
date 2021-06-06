from aiohttp import web
from marshmallow import Schema, fields, post_load
from . import common
from src.db import models as db
from src.db.models.Match import Match, MatchState
from src.serializers.match import MatchSchema
from src.io.match_manager import MatchManager
from src.api.middlewares.auth import auth_required 

routes = web.RouteTableDef()

# Coroutine called when server is launched after DB is set up
# This will ensure that for all NOT_STARTED matches, we will have a MatchManager
async def rebuild_match_managers(app):
  session = db.DBSession()
  qs = session.query(Match).filter(Match.state == MatchState.NOT_STARTED)

  for match in qs:
    manager = MatchManager(match)
    app['match_managers'][match.id] = manager    


# Coroutine called when the server shuts down
# All matches in progress will be put into state ENDED
async def cleanup_matches(app):
  session = db.DBSession()
  qs = session.query(Match).filter(Match.state != MatchState.NOT_STARTED, Match.state != MatchState.ENDED)

  for match in qs:
    await app['match_managers'][match.id].end()
    match.state = MatchState.ENDED

  session.commit()

@routes.view("/match")
class MatchApi(web.View):
  schema = MatchSchema()

  async def get(self):
    session = db.DBSession()
    qs = session.query(Match).all()
    return web.json_response(self.schema.dump(qs, many=True))

  @auth_required
  async def post(self):
    data = await self.request.json()
    match = self.schema.load(data)
    match.firstSideT = 0
    match.firstSideCT = 0
    match.secondSideT = 0
    match.secondSideCT = 0
    match.firstSideTerrorist = 'A'
    match.mapSelectionMode = 'rng'
    match.state = MatchState.NOT_STARTED

    session = db.DBSession()
    try:
      session.add(match)
      session.commit()    
    except:
      session.rollback()
      raise

    manager = MatchManager(match)
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

  async def _process_update(self, manager, current_match, key, value):

    if key == 'state':
      if value == 'STARTING' and current_match.state == MatchState.NOT_STARTED:
        await manager.setup()
      
      elif value == 'ENDED' and current_match.state != MatchState.NOT_STARTED:
        await manager.end()

  async def patch(self):
    _id = await self.get_object_id()
    data = await self.request.json()

    # HACK: exactly the same thing as schema.validate (validate against marshmallow without serializing)
    # but directly raise marshmallow ValidationError instead of returning a dict of validation errors
    self.schema._do_load(data, partial=True, postprocess=False)

    try:
      session = db.DBSession()
      match = session.query(Match).filter(Match.id == _id).one()

      if not _id in self.request.app['match_managers']:
        raise Exception("Match manager does not exist for match id {}".format(_id))

      manager = self.request.app['match_managers'][_id]

      for key, value in data.items():
        await self._process_update(manager, match, key, value)
        setattr(match, key, value)

      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.schema.dump(match))

  
  @auth_required
  async def delete(self):
    _id = await self.get_object_id()

    try:
      session = db.DBSession()
      match = session.query(Match).filter(Match.id == _id).one()
      
      if match.state not in [MatchState.NOT_STARTED, MatchState.ENDED]:
        if not _id in self.request.app['match_managers']:
          raise Exception("Match manager does not exist for match id {}".format(_id))

        await self.request.app['match_managers'][_id].end()

      session.delete(match)

      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response({"success": "the match has been deleted"}, status=200)
