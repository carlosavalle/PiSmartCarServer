import socket
import sys

class SocketServer2:

    def __init__(self,Host,Port):
        self.host = Host
        self.port = Port
        

    def Connect2(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(10)
        return s


