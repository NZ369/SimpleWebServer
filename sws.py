#!/usr/bin/python

# CSC 361 WINTER 2020 */
# Assignment #1 */
# Student name: Yuying Zhang (Nina) */
# Student #: V00924070 */


import sys, getopt, os.path
from socket import *
from select import *
from datetime import datetime

httpRequest = ''
connectionResponse = ''

# Function: Opens the file through passed parameters, creates the message and sends it
def openFile(path, clientSocket):
    global connectionResponse
    path = os.getcwd()+path
    if (os.path.isfile(path)):
        file = open(path,"r")
        msg = "\nHTTP/1.0 200 OK\n\n"
        connectionResponse = msg
        contents = file.readlines()
        for line in contents:
            msg += line
        msg += "\n\n"
        clientSocket.sendall(bytes(msg, 'utf-8'))
    else:
        msg = "\nHTTP/1.0 404 Not Found\n\n"
        connectionResponse = msg
        clientSocket.send(bytes(msg, 'utf-8'))

# Function: Parses and checks the first input line from the user
def parseHTTPCommand(clientCommands):
    global httpRequest
    httpRequest = clientCommands
    firstLine = clientCommands.splitlines()[0]
    firstLine = clientCommands.rstrip('\r\n')
    (request,  # GET
    path,     # /hello
    version  # HTTP/1.0
    ) = firstLine.split()

    if (request != "GET" or version != "HTTP/1.0"):
        return ""
    else:
        return path

# Function: Parses and checks the second input line from the user
def parseConnection(clientCommands):
    firstLine = clientCommands.splitlines()[0]
    firstLine = clientCommands.rstrip('\r\n').lower()
    (request,       # Connection:
    conn_option,    # keep-alive or close
    ) = firstLine.split(':')

    if (request == 'connection'):
        if (conn_option == 'keep-alive'):
            return 1
        elif (conn_option == 'close'):
            return 0
    return -1

# Function: Takes in the clientAddress parameters and outputs a time stamp for each client serviced
def connectionEnd(ip, port):
    global httpRequest, connectionResponse
    currTime = datetime.now()
    timeStamp = currTime.strftime("%a %b %d %H:%M:%S PDT 2020")
    msg = timeStamp + ": " + str(ip) + ":" + str(port) + " " + httpRequest + "; " + connectionResponse.strip('\n')
    print(msg)

# Function: Outputs a bad request message
def badRequest(clientSocket):
    global connectionResponse
    msg = "\nHTTP/1.0 400 Bad Request\n"
    connectionResponse = msg
    clientSocket.send(bytes(msg, 'utf-8'))

# Function: Processes the input from connected clients
def processInput(clientSocket):
    connectionType = 1;
    # Ensures persistent connection if selected
    while (connectionType == 1):

        read = clientSocket.makefile('r')
        write = clientSocket.makefile('w')

        registeringCommands = 0;
        httpCommand = '';

        while ( registeringCommands < 3 ):
            clientInput = read.readline()
            if not clientInput: break;
            command = clientInput.strip()
            request = command
            if (registeringCommands == 0):
                httpCommand = parseHTTPCommand(command)
            elif (registeringCommands == 1):
                try:
                    connectionType = parseConnection(command)
                except:
                    connectionType = 0
            registeringCommands += 1
                
        if(httpCommand == '' or connectionType == -1):
            badRequest(clientSocket)
            break;
        else:
            openFile(httpCommand, clientSocket)
            if (connectionType == 1):
                continue

    # Closes connection if non-persistent
    if (connectionType == 0):
        clientSocket.close()

# Function: In charge of creating multiple processes to serve each connected client
def serveForever(ipAddress, portNumber):
    #Creates a TCP connection of IPv4
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', portNumber))
    serverSocket.listen(5)

    while True:
        print("<<<  Server in operation  >>>")
        clientSocket, clientAddress = serverSocket.accept()
        print(f"Recieved connection from IP {clientAddress[0]}: Port {clientAddress[1]}.")

        pid = os.fork()

        if pid == 0:
            serverSocket.close()
            try:
                processInput(clientSocket)
            except:
                badRequest(clientSocket)
            connectionEnd(clientAddress[0], clientAddress[1])
            clientSocket.close()
            os._exit(0)
        else:
            clientSocket.close()

# Main: Starts the server
if __name__ == '__main__':
    ipAddress = sys.argv[1]
    portNumber = int(sys.argv[2])
    serveForever(ipAddress, portNumber)