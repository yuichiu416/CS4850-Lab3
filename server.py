import socket
from threading import Thread

users = []
passwords = []
activeUsers = []
loginInfo = {}
clients = {}
addresses = {}

with open('users.txt') as file:
    for line in file:
        line = line.replace("\n", "")
        fields = line.split(' ')
        users.append(fields[0])
        passwords.append(fields[1])
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 13381
sock.bind((host, port))
MAXCLIENTS = 3

sock.listen(MAXCLIENTS)
conn = None

currUser = ''
'''def accept_incoming_connections():
    while True:

        print("running")
        client, client_address = sock.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the Roger! Now type your name and password and press enter!", "utf8"))
        # addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def client_thread(conn):
    conn.send("Welcome to the Server. Type messages and press enter to send.\n")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        reply = "OK . . " + data
        conn.sendall(reply)
    conn.close()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(1024).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type :q to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)
'''
def login(conn, cmd):
    global currUser, activeUsers
    for i in range(0, len(users)):
        if (users[i] == cmd[1] and passwords[i] == cmd[2]):
            response = 'Server: ' + users[i] + ' joins.'
            currUser = users[i]
            activeUsers.append(currUser)
            print("activeUsers added: ", currUser)
            print(currUser + ' login.')
            return response
    if (currUser != True):
        return 'Incorrect UserID/Password.'
def newuser(conn, cmd):
        createNewUser = True
        # for user in users:
        for i in range(1, len(users)):
            # if (user['UserID'] == cmd[1]):
            if (users[i] == cmd[1]):
                response = 'Server: ' + users[i] + ' already exists. Please try a different username.'
                conn.send(response.encode('utf-8'))
                createNewUser = False
                break
        if (createNewUser == True):
            if (len(cmd[1]) < 32 and len(cmd[2]) >= 4 and len(cmd[2]) <= 8):
                # users.append({'UserID' : cmd[1], 'Password' : cmd[2]})
                with open("users.txt", "a") as userFile:
                    userFile.write(cmd[1] + ' ' + cmd[2] + "\n")
                    userFile.close()
                response = 'User ' + cmd[1] + ' created successfully.'
                return response
            else:
                return 'The length of the UserID should be less than 32, and the length of the Password should be between 4 and 8 characters.'
def sendAll(conn, cmd):
    cmd.remove(cmd[0])
    cmd.remove(cmd[1])
    msg = ' '.join(cmd)
    msg = "<sending all>: " + currUser + ': ' + msg
    conn.sendall(msg.encode('utf-8'))
    print(msg)
    return ''
def send(conn, cmd):
    cmd.remove(cmd[0])
    msg = ' '.join(cmd)
    msg = currUser + ': ' + msg
    print('msg is', msg)
    return msg

def who():
    pass

def logout():
    global currUser, activeUsers
    msg = 'Server: ' + currUser + ' left.'
    conn.send(msg.encode('utf-8'))
    print(currUser + ' logout.')
    activeUsers.remove(currUser)
    print('removed', currUser, 'from active users')
    currUser = ''
    return ''

def switcher(conn, msg):
    cmd = msg.split()
    if len(cmd) > 2 and cmd[0] == "login":
        if currUser != '':
            return 'User ' + currUser + ' is already logged in. Please logout first if you wish to login as a differnt user.'
        return login(conn, cmd)
    elif len(cmd) > 2 and cmd[0] == "newuser":
        return newuser(conn, cmd)
    elif len(cmd) > 3 and cmd[0] == "send" and cmd[1] == "all":
        if (currUser == ''):
            return 'Denied. Please login in first.'
        return sendAll(conn, cmd)
    elif len(cmd) > 2 and cmd[0] == "send":
        if (currUser == ''):
            return 'Denied. Please login in first.'
        return send(conn, cmd)
    elif len(cmd) == 1 and cmd == "who":
        return who(conn, cmd)
    elif cmd[0] == "logout":
        if (currUser == ''):
            return "No user is currently logged in."
        return logout()
    else:
        return "Unknown command, or incorrect usage of command. Please try again."

while True:
    if (conn is None):
        print('Running on host:', host, 'port: ', port)
        print('[Waiting for connection...]')
        conn, addr = sock.accept()
        print('Got connection from', addr)
    else:
        print("[-] Connected to " + addr[0] + ":" + str(addr[1]))
        # start_new_thread(client_thread, (conn,))
        try:
            msg = (conn.recv(1024)).decode('utf-8')
            msg = switcher(conn, msg)
            conn.send(msg.encode('utf-8'))
            print(msg)
        except:
            print("there's an error, please check the connection.")
sock.close()
