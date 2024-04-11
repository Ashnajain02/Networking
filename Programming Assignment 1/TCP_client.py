from socket import *
from datetime import datetime
import sys

#get arguments from command line
serverIP = sys.argv[2]
serverPort = sys.argv[3]
connectionID = sys.argv[4]

#creating internet socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#function that takes in a connectionID, and sends a message to the server
def sendMessage(connectionID):
   clientSocket = socket(AF_INET, SOCK_STREAM) 
    #if no client attempts to connect then server will error
    try:
        clientSocket.connect((serverIP, int(serverPort)))
    except ConnectionRefusedError:
        print("ConnectionRefusedError")
        return ['FAIL']
    print("client and server are now connected @ {}".format(datetime.now()))
    #construct message to be send
    message = 'HELLO ' + connectionID
    clientSocket.send(message.encode())
    clientSocket.settimeout(15.0)
    print("<- client sent {} to the server @ {}".format(message, datetime.now()))
    #if client does not receive a response of 15 seconds, it timesout 
    try: 
        modifiedMessage = clientSocket.recv(1024)
    except:
        return ['RESET']
    #reformat message that the client receives
    print(modifiedMessage.decode())
    modifiedMessage = modifiedMessage.decode().split(" ")
    return modifiedMessage


result = sendMessage(connectionID)


if result[0] == 'FAIL':
    print("Connection Failure ", datetime.now())
else:
    attempt = 1
    #keep allowing the user to reconnect until we establish a connection or, we have exceeded 3 attempts
    while(result[0] != 'OK' and attempt <= 3):
        print("Connection error ", connectionID, " ", datetime.now())
        connectionID = input('Enter in a new connectionID: ')
        result = sendMessage(connectionID)
        attempt += 1
    #if attempt is 4 then its a connection Failure
    if(attempt == 4):
        print("Connection Failure ", datetime.now())
    else: #otherwise its connection established
        print("Connection established ", connectionID, serverIP, serverPort, datetime.now())

clientSocket.close()