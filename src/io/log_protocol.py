import asyncio
import struct
import logging


class CSGOLogProtocol(asyncio.DatagramProtocol):
  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def connection_made(self, transport):
    self.transport = transport

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
    
    message = data[7:-2].decode()
    self.logger.warning("Received RCON message from {}: '{}'".format(addr, message))

    # TODO: call parser and call handling routine

