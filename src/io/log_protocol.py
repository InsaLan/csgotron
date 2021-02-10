import asyncio
import struct
import logging
from ..message.parser import MonParser, BadMessageException

class CSGOLogProtocol(asyncio.DatagramProtocol):
  def __init__(self, match_manager):
    self.logger = logging.getLogger(__name__)
    self.match_manager = match_manager
    self.parser = MonParser()

  def connection_made(self, transport):
    self.transport = transport
    sockname = transport.get_extra_info('sockname')
    self.logger.debug('Log protocol is now listening on {} for match {}'.format(sockname, self.match_manager.match))

  def datagram_received(self, data, addr):
    # the log protocol seem to be inspired from https://developer.valvesoftware.com/wiki/Server_queries

    header = struct.unpack('iccc', data[0:7])    
    footer = struct.unpack('cc', data[-2:])

    if not header == (-1, b'R', b'L', b' '):
      # log malformed message, bad header
      print("malformed message received, bad header {}".format(header))
      return

    if not footer == (b'\n', b'\x00'):
      print("malformed message received, bad footer {}".format(footer))
      return
    
    timestamp = data[7:28].decode()
    message = data[30:-2].decode()

    #self.logger.debug("Recv log from {}, timestamp: '{}', message: '{}'".format(addr, timestamp, message[:65] + (message[65:] and '...')))

    try:
      x = self.parser.parse(message)
      #self.logger.info("MESSAGE HANDLED {}".format(x))
    except BadMessageException:
      self.logger.warning("Message '{}' at timestamp: '{}' was not handled by parser".format(message[:65] + (message[65:] and '...'),timestamp))
