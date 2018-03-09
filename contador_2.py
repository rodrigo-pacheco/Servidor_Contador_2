#!/usr/bin/python3
"""
Contador Server: serves inverse counter: 5,4,3,2,1,0,5

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ gsyc.es
SAT subject (Universidad Rey Juan Carlos)
"""

import socket

NUMBER = 0

# Reverse counter
def nextnumber():
    global NUMBER
    if NUMBER == 0:
        NUMBER = 5
        return(str(NUMBER))
    else:
        NUMBER = NUMBER -1
        return(str(NUMBER))

# Parse petition
def parse(received):
    try:
        method = received.split()[0]
        resource = received.split()[1]
        return(method, resource)
    except:
        return('', '')

# Process petition
def process(request):
    if request[0] == 'GET':
        if request[1] == '/contador':
            return('200 OK',nextnumber())
        else:
            return('404 Not Found' ,'Resource not found')
    else:
        return('404 Not Found', 'Only answers to GET requests')

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests
mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        print('Answering back...')

        received = str(recvSocket.recv(2048), 'utf-8')
        request = parse(received)
        code, answer = process(request)

        recvSocket.send(bytes(
                        'HTTP/1.1 ' + code + '\r\n\r\n' +
                        '<html><body><h1>Welcome to online reverse counter</h1>' +
                        answer +
                        '</body></html>' +
                        '\r\n', 'utf-8'))
        recvSocket.close()

except KeyboardInterrupt:
    print("Closing binded socket")
    mySocket.close()
