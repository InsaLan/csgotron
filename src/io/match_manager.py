import asyncio
import logging
from aiorcon import RCON

from ..db import models as db
from ..db.models.Match import Match
from .log_protocol import CSGOLogProtocol

class MatchManager:
  confinebot_ip = '10.0.0.157'
  next_log_port = 25555
  
  def __init__(self, match):
    self.match = match
    self.logger = logging.getLogger(__name__)

  async def _update_match(self):
    self.session = db.DBSession()
    self.match = self.session.query(Match).filter(Match.id == self.match.id).one()

  async def setParameters(self):
    await self._update_match()

    await(self.rcon("mp_overtime_maxrounds {}".format(self.match.maxRound)))

    if self.match.overtime:
      await(self.rcon("mp_overtime_enable 1"))

    await(self.rcon("mp_teamname_1 \"{}\"".format(self.match.teamA.name)))
    await(self.rcon("mp_teamname_2 \"{}\"".format(self.match.teamB.name)))

  async def setup(self):
    self.logger.info("Setting up match id={}".format(self.match.id))
    loop = asyncio.get_event_loop()

    # setup RCON
    self.rcon = await RCON.create(str(self.match.server.ip), self.match.server.port, self.match.password, loop)
   
    self.log_port = MatchManager.next_log_port
    MatchManager.next_log_port += 1
 
    # setup log listener
    self.log_transport, _ = await loop.create_datagram_endpoint(lambda: CSGOLogProtocol(self),
                                                    local_addr=('0.0.0.0', self.log_port))

    # send setup RCON commands
    await(self.rcon("log on; mp_logdetail 3;"))
    await(self.rcon("logaddress_del {}:{}; logaddress_add {}:{}".format(MatchManager.confinebot_ip, self.log_port, MatchManager.confinebot_ip, self.log_port)))

    await self.setParameters()    

  async def end(self):
    # kill log listener
    self.log_transport.close()

    # close RCON
    self.rcon.close()
