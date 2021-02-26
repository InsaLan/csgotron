import asyncio
import logging
from aiorcon import RCON

from src.config import ConfigStore
from src.db import models as db
from src.db.models.Match import Match
from src.io.log_protocol import CSGOLogProtocol

config = ConfigStore.cfg

class MatchManager:
  next_log_port = config.log_port_range[0]
  
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
      await self.rcon("mp_overtime_enable 1")

    await(self.rcon("mp_teamname_1 \"{}\"".format(self.match.teamFirstSideT.name)))
    await(self.rcon("mp_teamname_2 \"{}\"".format(self.match.teamFirstSideCT.name)))

  async def setup(self):
    self.logger.info("Setting up match id={}".format(self.match.id))
    loop = asyncio.get_event_loop()

    # setup RCON
    self.rcon = await RCON.create(str(self.match.server.ip), self.match.server.port, self.match.password, loop, timeout=1, auto_reconnect_attempts=0)

    self.log_port = MatchManager.next_log_port
    if (MatchManager.next_log_port + 1) < config.log_port_range[1]:
      # FIXME: when match has ended, the port needs to be freed, the port allocation mechanism needs to be changed,
      # but this is fine for testing
      self.logger.error("Allocated all log ports in range! bad things may happen following this")

    MatchManager.next_log_port += 1
 
    # setup log listener
    self.log_transport, _ = await loop.create_datagram_endpoint(lambda: CSGOLogProtocol(self),
                                                    local_addr=(str(config.listen_addr), self.log_port))

    # send setup RCON commands
    await(self.rcon("log on; mp_logdetail 3;"))
    
    print("xxx",config.listen_addr, self.log_port)
    await(self.rcon("logaddress_del {}:{}; logaddress_add {}:{}".format(config.listen_addr, self.log_port, config.listen_addr, self.log_port)))
    await self.setParameters()    

  async def end(self):
    # kill log listener
    self.log_transport.close()

    # close RCON
    self.rcon.close()
