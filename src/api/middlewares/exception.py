import json
import logging

from aiohttp import web
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

logger = logging.getLogger(__name__)

# https://gist.github.com/amitripshtos/854da3f4217e3441e8fceea85b0cbd91

def json_error(http_status: int,
               exception: Exception,
               error_name = None,
               error_desc = None,
               error_additional = {}) -> web.Response:

    logger.exception(exception)

    payload = {
      'error': {
        'name': error_name if (error_name) else exception.__class__.__name__, 
      }
    }

    if (error_desc):
      payload['error']['desc'] = error_desc
    
    if (len(error_additional) > 0):
      payload['error']['additional'] = error_additional
    
    return web.json_response(payload, status=http_status)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
      if ex.status == 404:
          return json_error(ex.status, ex, error_name='NotFound')
      raise
    except NoResultFound as e:
      return json_error(404, e, error_name='NotFound')
    except ValidationError as e:
      return json_error(400, e, error_additional=e.messages)
    except Exception as e:
        return json_error(500, e, error_desc=str(e))

