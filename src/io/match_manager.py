from aiorcon import RCON

class MatchManager:

  def __init__(match_id):
    self.id = match_id
    self.rcon = None

  def setup():
    # setup RCON
    self.rcon = await RCON.create("192.168.2.137", 27015, "rconpassword", loop)
    
    # setup log listener
    
    # send setup RCON commands
    await(self.rcon("log on; mp_logdetail 3;"))


  def end():
    # kill log listener

    # close RCON
    self.rcon.close()
