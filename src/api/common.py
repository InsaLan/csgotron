from aiohttp import web
from marshmallow import Schema, fields, post_load
def patch_object(obj, patch):
  for key, value in patch.items():
    setattr(obj, key, value)


class DetailsApi(web.View):
  async def get_object_id(self):
    _id = self.request.match_info.get('id', None)
    _id = int(_id) if _id.isnumeric() else None

    if _id == None:
      raise

    return _id    

