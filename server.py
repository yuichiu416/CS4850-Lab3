# Roger Kiew, 14283381, rkry8
# CS 4850 Lab 3 version 2
# Multiuser chatroom
# Server script

import socket, threading

# global variables
users = []
passwords = []
activeUsers = {}
serverRunning = True
currUser = ''
clientAddresses = {}
conns = {}
sock = ''
host = ''
port = ''
MAXCLIENTS = 3
conn = ''
loggedIn = False

#helper functions
def commandValidate(conn, msg):
    cmd = msg.split()
    if len(cmd) > 2 and cmd[0] == "login":
        return True
    elif len(cmd) > 2 and cmd[0] == "newuser":
        return True
    elif len(cmd) > 2 and cmd[0] == "send" and cmd[1] == "all":
        return True
    elif len(cmd) > 2 and cmd[0] == "send":
        return True
    elif len(cmd) > 1 and cmd[0] == "send":
        return True
    elif len(cmd) == 1 and cmd[0] == "who":
        return True
    elif cmd[0] == "logout":
        return True
    else:
        msg = "Unknown command or incorrect usage of command. Please try again."
        sendMsg(conn, msg)
        print(msg)
        return False

    msg = "Unknown command, or incorrect usage of command. Please try again."
    return False
    return True
def getCurrentUser(conn):
    for key in activeUsers:
        if(conn == activeUsers[key]):
            return key

def isLoggedIn(conn):
    for key in activeUsers:
        if(activeUsers[key] == conn):
            return True
    return False

# reload the user.txt and refresh the data if necessary
def reloadLoginFile():
    global  users , passwords, activeUsers
    with open('users.txt', 'r') as file:
        for line in file:
            if(line):
                line = line.replace("\n", "")
                line = line.replace("\r", "")
                fields = line.split(' ')
                if(fields[0] not in users):
                    users.append(fields[0])
                if(fields[1] not in passwords):
                    passwords.append(fields[1])
                if(fields[0] not in activeUsers):
                    activeUsers.update({fields[0]: ''})
        file.close()

# send message to assigned connection
def sendMsg(conn, msg):
    conn.send(msg.encode('utf-8'))

# set up the server
def setup():
    global sock, host, port
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 13381
    sock.bind((host, port))
    MAXCLIENTS = 3
    sock.listen(MAXCLIENTS)

# required functions
def login(conn, cmd):
    global activeUsers, addr
    i = 0
    reloadLoginFile()
    for key in activeUsers:
        if(conn == activeUsers[key]):
            msg = 'Please log out first.'
            sendMsg(conn, msg)
            return ''
    for key in activeUsers:
        if(cmd[1] == key and activeUsers[key] != ''):
            msg = 'User ' + key + ' is already logged in. Please logout first if you wish to login as a different user.'
            sendMsg(conn, msg)
            return ''
        if (users[i] == cmd[1] and passwords[i] == cmd[2]):
            currUser = users[i]
            activeUsers.update({currUser: conn})
            msg = 'logged in.'
            for key in activeUsers:
                if(conn == activeUsers[key]):
                    sendMsg(activeUsers[key], msg)
            return currUser +' joined the server.'
        i += 1
    msg = 'Incorrect UserID/Password.'
    for key in activeUsers:
        if(activeUsers[key] != '' and conn == activeUsers[key]):
            sendMsg(activeUsers[key], msg)
    msg = 'Bad login attempt from: ' + host
    sendMsg(conn, msg)
    return msg

def newuser(conn, cmd):
    createdUser = False
    reloadLoginFile()
    for i in range(0, len(users)):
        if (users[i] == cmd[1]):
            msg = 'Server: ' + users[i] + ' already exists. Please try a different username.'
            sendMsg(conn, msg)
            createNewUser = False
            return msg
    if (len(cmd[1]) < 32 and len(cmd[2]) >= 4 and len(cmd[2]) <= 8):
        with open('users.txt', 'r') as file:
            lines = file.read()
            file.close()
            with open('users.txt', 'w') as file:
                file.write(lines)
                file.write('\n' + cmd[1] + ' ' + cmd[2])
                file.close()

        msg = 'User ' + cmd[1] + ' created successfully by' + host
        sendMsg(conn, msg)
        createdUser = True
        return msg
    else:
        msg = 'The length of the UserID should be less than 32, and the length of the Password should be between 4 and 8 characters.'
        sendMsg(conn, msg)
        return ''

def sendAll(conn, cmd):
    global activeUsers
    cmd.remove(cmd[0]) # before: send  all <message>
    cmd.remove(cmd[0]) # before: all <message>
    msg = ' '.join(cmd) # <message>
    currUser = getCurrentUser(conn)
    msg = currUser + "<sending all>" + ': ' + msg
    for key in activeUsers:
        if(activeUsers[key] != ''):
            sendMsg(activeUsers[key], msg)
    print(msg)
    return ''

def sendUser(conn, cmd):
    cmd.remove(cmd[0])#before: send userID <message>
    target = cmd[0] #before: userID <message>
    cmd.remove(cmd[0])
    currUser = getCurrentUser(conn)
    msg = currUser + ' to ' + target + ': '+ cmd[0]
    sendMsg(activeUsers[target], msg)
    sendMsg(activeUsers[currUser], msg)

def send(conn, cmd):
    cmd.remove(cmd[0])
    msg = ' '.join(cmd)
    msg = currUser + ': ' + msg
    for key in activeUsers:
        if(activeUsers[key]):
            sendMsg(activeUsers[key], msg)
    return msg

def who(conn, cmd):
    global activeUsers
    reloadLoginFile()
    currUser = getCurrentUser(conn)
    msg = 'Users in the chatroom: '
    sendMsg(conn, msg)
    for key in activeUsers:
        if(activeUsers[key] != ''):
            sendMsg(activeUsers[currUser], key)
    return ''

def logout(conn):
    global activeUsers
    for key in activeUsers:
        if(conn == activeUsers[key]):
            activeUsers.update({key : ''})
            msg = 'logged out'
            sendMsg(conn, msg)
            msg = key + ' left'
            break
    return msg

def switcher(conn, msg):
    if(not commandValidate(conn, msg)):
        return
    cmd = msg.split()
    if cmd[0] == "login":
        return login(conn, cmd)
    elif cmd[0] == "newuser":
        return newuser(conn, cmd)
    if (not isLoggedIn(conn)):
        msg = 'Without logging in, the only supported commands are "login" and "newuser"'
        return sendMsg(conn, msg)
    elif cmd[0] == "send" and cmd[1] == "all":
        return sendAll(conn, cmd)
    elif len(cmd) > 2 and cmd[0] == "send":
        return sendUser(conn, cmd)
    elif len(cmd) > 1 and cmd[0] == "send":
        return send(conn, cmd)
    elif cmd[0] == "who":
        return who(conn, cmd)
    elif cmd[0] == "logout":
        return logout(conn)
    else:
        msg = "Unknown command, or incorrect usage of command. Please try again."
        return sendMsg(conn, msg)

def handleClient(conn, addr):
    global activeUsers
    clientConncted = True
    while(clientConncted):
        try:
            msg = conn.recv(1024).decode('utf-8')
            msg = switcher(conn, msg)
            if(msg != None):
                print(msg)
        except:
            print("there's an error, please check the connection.")
            clientConncted = False

def runServer():
    global host, port, conn, addr
    print('Running on host:', host, 'port: ', port)
    while(serverRunning):
        print('[Waiting for connection...]')
        conn, addr = sock.accept()
        print('Got connection from', addr[0],  ":", str(addr[1]))

        if(addr not in clientAddresses):
            clientAddresses[addr] = addr
            conns[conn] = conn
            threading.Thread(target= handleClient, args = (conn, addr)).start()

def main():
    setup()
    runServer()
    sock.close()

if __name__ == "__main__":
    main()
