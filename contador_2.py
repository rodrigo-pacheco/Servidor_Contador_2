#!/usr/bin/python3
"""
Contador Server: serves inverse counter: 5,4,3,2,1,0,5

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ gsyc.es
SAT subject (Universidad Rey Juan Carlos)
"""

import socket

USERS = {}
LAST_USER = 0


# Creates and adds user to dictionary
def create_user():
    global USERS
    global LAST_USER
    LAST_USER = LAST_USER + 1
    USERS['/contador/' + str(LAST_USER)] = 0
    print('DiccionARIO')
    print(USERS)
    return LAST_USER


# Reverse counter
def next_number(previous):
    previous = int(previous)
    if previous == 0:
        return(str(5))
    else:
        print(type(previous))
        current = previous - 1
        return(str(current))


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
    global USERS
    if request[0] == 'GET':
        if request[1] == '/contador':
            user_id = create_user()
            return('200 OK', "<a href=/contador/" + str(user_id) + ">Obtain your number</a>")
        elif request[1] in USERS:
            counter = next_number(USERS[request[1]])
            USERS[request[1]] = counter
            return('200 OK', str(counter))
        else:
            return('404 Not Found', 'Resource not found')
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
