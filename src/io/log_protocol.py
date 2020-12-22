import asyncio
import struct

class CSGOLogProtocol(asyncio.DatagramProtocol):
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
    print('Received %r from %s' % (message, addr))

    # TODO: call parser and call handling routine

#async def main():
#  t = await loop.create_datagram_endpoint(
#    lambda: CSGOLogProtocol(),
#    local_addr=('10.0.0.113', 8888))
#  
#  print("Server created")
#
#loop = asyncio.get_event_loop() 
#loop.run_until_complete(main())
#loop.run_forever()
