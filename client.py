# Roger Kiew, 14283381, rkry8
# CS 4850 Lab 3 version 2
# Multiuser chatroom
# Client script
import socket, threading, sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 13381

try:
    sock.connect((host, port))
    print ('Connected to', host)
except:
    print('Unable to connect\n')
    sys.exit()

clientRunning = True

def receiveMsg(sock):
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            msg = sock.recv(1024).decode('utf-8')
            print(msg)
        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            serverDown = True

threading.Thread(target = receiveMsg, args = (sock,)).start()

while (clientRunning):
    msg = input()
    sock.sendall(msg.encode('utf-8'))
    if (msg == ':q'):
        break
print("Quiting, shutting down...")
sock.close()
