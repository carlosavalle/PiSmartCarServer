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


#HOST = '192.168.111.10' #this is your localhost
#PORT = 888

#socket.socket: must use to create a socket.
#socket.AF_INET: Address Format, Internet = IP Addresses.
#socket.SOCK_STREAM: two-way, connection-based byte streams.
#print ('socket created')
 
#Bind socket to Host and Port
 
 
#listen(): This method sets up and start TCP listener.

