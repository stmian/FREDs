_author_ = 'Darshan Kothari'

import json
import socket
import struct
import logging

logger = logging.getLogger("jsonSocket")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime) -15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class JsonSocket(object):
    def __init__(self, address='localhost', port=80):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port

    def sendObj(self, obj):
        msg = json.dumps(obj)
        print msg
        if self.socket:
            frmt = "=%ds" % len(msg)
            packedMsg = struct.pack(frmt, msg)
            packedHdr = struct.pack('=I', len(packedMsg))

            self._send(packedHdr)
            self._send(packedMsg)

    def _send(self, msg):
        sent = 0
        while sent < len(msg):
            sent += self.conn.send(msg[sent:])

    def _read(self, size):
        data = ''
        while len(data) < size:
            dataTmp = self.conn.recv(size -len(data))
            data += dataTmp
            if dataTmp == '':
                raise RuntimeError("socket connection may have be broken")
        return data

    def _msgLength(self):
        d = self._read(4)
        s = struct.unpack('=I', d)
        return s[0]

    def readObj(self):
        size = self._msgLength()
        data = self._read(size)
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return json.loads(msg[0])

    def close(self):
        logger.debug("closing main socket")
        self._closeSocket()
        if self.socket is not self.conn:
            logger.debug("closing connection socket")
            self._closeConnection()

    def _closeSocket(self):
        self.socket.close()

    def _closeConnection(self):
        self.conn.close()

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass