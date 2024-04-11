from socket import *
from datetime import datetime
import sys
import threading as th

inuse_IDs = set()

#function that removes ID from inuse_IDs set
def removeID(ID):
    inuse_IDs.remove(ID)
    print(inuse_IDs)

serverIP = sys.argv[1]
serverPort = sys.argv[2] 

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',int(serverPort)))
serverSocket.listen(1)
print('The TCP server is ready to receive')
serverSocket.settimeout(120.0)

while True:
     try:
         connectionSocket, addr = serverSocket.accept()
         print("--> server accepted a connection from {} @ {}".format(addr, datetime.now()))
     except:
         print("Server Time Out")
         break
     
     message = connectionSocket.recv(1024)
     print("--> server received {} @ {}".format(message.decode(), datetime.now()))
     message = message.decode().split(" ")
     connectionID = message[1]
     clientIP = addr[0]
     clientPort = addr[1]
     
     if connectionID in inuse_IDs:
        response = "RESET" + " " + connectionID
     else:
        inuse_IDs.add(connectionID)
        T = th.Timer(30.0, removeID, [connectionID])
        T.start()
        response = "OK" + " " + connectionID + " " + clientIP + " " + str(clientPort)
     
     connectionSocket.send(response.encode())
     print("<- server sent {} @ {}".format(response, datetime.now()))

     connectionSocket.close()

serverSocket.close()