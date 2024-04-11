from socket import *
from datetime import datetime
import sys
import threading as th

inuse_IDs = set()

#function that removes a ID from inuse_IDs dict
def removeID(ID):
    inuse_IDs.remove(ID)
    print(inuse_IDs)

#getting information from command line
serverIP = sys.argv[1]
serverPort = sys.argv[2]

#binding socket to internet and server IP/Port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', int(serverPort)))
print("The UDP server is ready to receive")
#server will time out if it doesnt receive a connection after 2 minutes
serverSocket.settimeout(120.0)

while True:
    try: #try sending message 
        message, clientAddress = serverSocket.recvfrom(2048) # if the buf size value is smaller than the datagram size, it will drop the rest.
        print("--> server received {} from {} @ {}".format(message.decode(), clientAddress, datetime.now()))
    except: #if message cant be sent then...
        print("Server Time Out")
        break
   
    #reformat message so that it is an array 
    message = message.decode().split(" ")
    connectionID = message[1]
    clientIP = clientAddress[0]
    clientPort = clientAddress[1]
    
    #check if connectionID in in array, and act accordingly 
    if connectionID in inuse_IDs:
        response = "RESET" + " " + connectionID
    else:
        inuse_IDs.add(connectionID)
        #create a timer thread for the connectioID that we added to inuse_IDs array
        T = th.Timer(30.0, removeID, [connectionID])
        T.start()
        response = "OK" + " " + connectionID + " " + clientIP + " " + str(clientPort)

    #send response message to the client
    serverSocket.sendto(response.encode(), clientAddress)
    print("<- server sent {} to {} @ {}".format(response, clientAddress, datetime.now()))
    