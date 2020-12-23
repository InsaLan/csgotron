import asyncio
from aiorcon import RCON

from ..db import models as db
from ..db.models.Match import Match
from .log_protocol import CSGOLogProtocol


class MatchManager:
  next_log_port = 25555
  confinebot_ip = '10.0.0.157'
  
  def __init__(self, match_id):
    self.id = match_id

  def _get_match(self):
    session = db.DBSession()
    return session.query(Match).filter(Match.id == self.id).one()

  async def setup(self):
    match = self._get_match()
    loop = asyncio.get_event_loop()

    # setup RCON
    self.rcon = await RCON.create(str(match.server.ip), match.server.port, match.password, loop)
   
    self.log_port = MatchManager.next_log_port
    MatchManager.next_log_port += 1
 
    # setup log listener
    self.log_transport = await loop.create_datagram_endpoint(lambda: CSGOLogProtocol(),
                                                    local_addr=(MatchManager.confinebot_ip, self.log_port))

    # send setup RCON commands
    await(self.rcon("log on; mp_logdetail 3;"))
    await(self.rcon("logaddress_del {}:{}; logaddress_add {}:{}".format(MatchManager.confinebot_ip, self.log_port, MatchManager.confinebot_ip, self.log_port)))

    await(self.rcon("say test"))

  async def end(self):
    # kill log listener
    self.log_transport.close()

    # close RCON
    self.rcon.close()
