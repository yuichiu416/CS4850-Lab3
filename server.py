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
clientAddresses = {}
conns = {}
sock = ''
host = ''
port = ''
MAXCLIENTS = 3
conn = ''

#helper functions
def checkOnlineNumber(conn):
    ctr = 0
    for key in activeUsers:
        if(activeUsers[key] != ''):
            ctr += 1
    return ctr

def commandValidate(conn, msg):
    cmd = msg.split()
    if len(cmd) == 3 and cmd[0] == "login" :
        return True
    elif len(cmd) == 3 and cmd[0] == "newuser":
        return True
    elif len(cmd) > 2 and cmd[0] == "send" and cmd[1] == "all":
        return True
    elif len(cmd) > 2 and cmd[0] == "send":
        return True
    elif len(cmd) > 1 and cmd[0] == "send":
        return True
    elif len(cmd) == 1 and cmd[0] == "who":
        return True
    elif len(cmd) == 1 and cmd[0] == "logout":
        return True
    else:
        msg = "Unknown command or incorrect usage of command. Please try again."
        sendMsg(conn, msg)
        return False

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
    sock.listen(MAXCLIENTS)

# required functions
def login(conn, cmd):
    global activeUsers, addr
    i = 0
    reloadLoginFile()
    if(checkOnlineNumber(conn) >= 3):
        sendMsg(conn, 'Exceed maximum client number!\nPlease try again when someone logged out.')
        return ''
    for key in activeUsers:
        if(conn == activeUsers[key]):
            sendMsg(conn, 'Please log out first.')
            return ''
    for key in activeUsers:
        if(cmd[1] == key and activeUsers[key] != ''):
            sendMsg(conn, 'User ' + key + ' is already logged in. Please login as a different user.')
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
    sendMsg(conn, 'Incorrect UserID/Password.')
    return 'Bad login attempt from: ' + host

def newuser(conn, cmd):
    reloadLoginFile()
    for i in range(0, len(users)):
        if (users[i] == cmd[1]):
            msg = 'Server: ' + users[i] + ' already exists. Please try a different username.'
            sendMsg(conn, msg)
            return msg
    if (len(cmd[1]) < 32 and len(cmd[2]) >= 4 and len(cmd[2]) <= 8):
        with open('users.txt', 'r') as file:
            lines = file.read()
            file.close()
            with open('users.txt', 'w') as file: # reload the files and write the new user information in the next line
                file.write(lines)
                file.write('\n' + cmd[1] + ' ' + cmd[2])
                file.close()

        msg = 'User ' + cmd[1] + ' created successfully by' + host
        sendMsg(conn, msg)
        return msg
    else:
        sendMsg(conn, 'The length of the UserID should be less than 32, and the length of the Password should be between 4 and 8 characters.')
        return ''

def sendAll(conn, cmd):
    global activeUsers
    cmd.remove(cmd[0]) # before: send  all <message>
    cmd.remove(cmd[0]) # before: all <message>
    msg = ' '.join(cmd) # <message>
    currUser = getCurrentUser(conn)
    for key in activeUsers:
        if(activeUsers[key] != ''):
            sendMsg(activeUsers[key], currUser + "<sending all>" + ': ' + msg)
    return ''

def sendUser(conn, cmd):
    if cmd[1] in activeUsers:
        cmd.remove(cmd[0])# before: send userID <message>
        target = cmd[0] # before: userID <message>
        cmd.remove(cmd[0])
        currUser = getCurrentUser(conn)
        msg1 = 'From ' + currUser + ': ' + ' '.join(cmd)
        msg2 = 'To ' + target + ': ' + ' '.join(cmd)
        sendMsg(activeUsers[target], msg1)
        sendMsg(activeUsers[currUser], msg2)
    else:
        send(conn, cmd)

def send(conn, cmd):
    cmd.remove(cmd[0])
    msg = ' '.join(cmd)
    msg = getCurrentUser(conn) + ': ' + msg
    for key in activeUsers:
        if(activeUsers[key]):
            sendMsg(activeUsers[key], msg)
    return msg

def who(conn, cmd):
    global activeUsers
    reloadLoginFile()
    currUser = getCurrentUser(conn)
    sendMsg(conn, 'Users in the chatroom: \n')
    for key in activeUsers:
        if(activeUsers[key] == conn):
            sendMsg(activeUsers[currUser], key + ' <me>\n')
            continue
        if(activeUsers[key] != ''):
            sendMsg(activeUsers[currUser], key + '\n')
    return ''

def logout(conn):
    global activeUsers
    for key in activeUsers:
        if(conn == activeUsers[key]):
            activeUsers.update({key : ''})
            sendMsg(conn, 'logged out')
            msg = key + ' left'
            break
    return msg

def switcher(conn, msg):
    if(not commandValidate(conn, msg)):
        return ''
    cmd = msg.split()
    if cmd[0] == "login":
        return login(conn, cmd)
    elif cmd[0] == "newuser":
        return newuser(conn, cmd)
    if (not isLoggedIn(conn)):
        return sendMsg(conn, 'Without logging in, the only supported commands are "login" and "newuser"')
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
        return sendMsg(conn, "Unknown command, or incorrect usage of command. Please try again.")

def handleClient(conn, addr):
    global activeUsers
    clientConncted = True
    while(clientConncted):
        try:
            msg = switcher(conn, conn.recv(1024).decode('utf-8'))
            if(msg != None):
                print(msg)
        except:
            print(str(addr) + " is disconnected.")
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
