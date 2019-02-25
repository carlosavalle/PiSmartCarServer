from  SocketServer2 import *

print ('Socket is now listening')
 
Ss = SocketServer2("localhost",79)


while 1:
    conn, addr = Ss.Connect2().accept()
    print ('Connect with ' + addr[0] + ':' + str(addr[1]))
    buf = conn.recv(64)
    print (buf.decode())
    Ss.Connect2().close()
