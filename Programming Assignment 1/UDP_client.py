import datetime
from socket import *
import sys

bufferSize = 2048

#Getting information from command line arguments
serverIP = sys.argv[2]
serverPort = sys.argv[3]
connectionID = sys.argv[4]

clientSocket = socket(AF_INET, SOCK_DGRAM)

# function that sends a message with a particular connectionID
def sendMessage(connectionID):
    message = 'HELLO ' + connectionID
    clientSocket.sendto(message.encode(), (serverIP, int(serverPort)))
    print("<- client sent {} to the server @ {}".format(message, datetime.datetime.now()))
    clientSocket.settimeout(15.0) #sets attribute for clientSocket
    #if server times out then it will return with RESET message
    try: 
        modifiedMessage, serverAddress = clientSocket.recvfrom(bufferSize)
    except TimeoutError:
        return ['RESET']
    print("--> server received {} @ {}".format(message.decode(), datetime.now()))
    #changing message into array that can be easily parsed
    modifiedMessage = modifiedMessage.decode().split(" ")
    return modifiedMessage

#sending out inital message
result = sendMessage(connectionID)
attempt = 1
#We only break our loop on 2 conditions: 
    #if we receive an OK or if our number of attemps is >= 3
#Otherwise, we ask user to re-enter a connectionID
while(result[0] != 'OK' and attempt <= 3):
    print("Connection error", connectionID, datetime.datetime.now())
    connectionID = input('Enter in a new connectionID: ') 
    result = sendMessage(connectionID)
    attempt += 1

#If we used all 4 attempts then we print connection failure
if(attempt == 4):
    print("Connection Failure ", datetime.datetime.now())
else: #connection as established
    print("Connection established ", connectionID, serverIP, serverPort, datetime.datetime.now())
clientSocket.close() 
