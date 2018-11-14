import socket

sock = socket.socket()
host = socket.gethostname()
port = 13381

sock.connect((host, port))
print ('Connected to', host)

while (True):
    msg = input('> ')
    sock.sendall(msg.encode('utf-8'))
    # Halts
    returnMsg = (sock.recv(1024)).decode('utf-8')
    print ('> ' + returnMsg)

    if (msg == ':q'):
        break
    ### End if z == ':q':
    elif (msg == 'logout' and returnMsg != 'No user is currently logged in.'):
        break
