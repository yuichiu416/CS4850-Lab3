# Roger Kiew, 14283381, rkry8
# CS 4850 Lab 3 version 2
# Multiuser chatroom
# Client script
import socket, threading, sys

#global variables
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 13381
clientRunning = False

def greeting():
    print('My chat room client. Version Two.')
    print('Avaiable commands:')
    print('login <UserID> <Password>')
    print('newuser <UserID> <Password>')
    print('send all <message>')
    print('send UserID <message>')
    print('send <message>')
    print('who')
    print('logout')
    print('quit')

def setup():
    global  sock, clientRunning
    greeting()
    try:
        sock.connect((host, port))
        print ('Connected to', host)
        clientRunning = True
    except:
        print('Unable to connect\n')
        sys.exit()

def receiveMsg(sock):
    global  clientRunning
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            msg = sock.recv(1024).decode('utf-8')
            print(msg)
        except:
            print('Server is Down. You are now Disconnected.')
            serverDown = True

def runServer():
    threading.Thread(target = receiveMsg, args = (sock,)).start()
    while (clientRunning):
        msg = input()
        if (msg == 'quit'):
            break
        sock.sendall(msg.encode('utf-8'))
    print("Quiting, shutting down...")
    sock.sendall('help me'.encode('utf-8'))
    sock.close()

def main():
    global sock, clientRunning
    setup()
    runServer()

if __name__ == "__main__":
    main()
