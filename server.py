import socket
import json

users = []
activeUsers = []

with open('users.txt') as file:
    for line in file:
        fields = line.split(' ')
        users.append(fields[0])

sock = socket.socket()
host = socket.gethostname()
port = 13381
sock.bind((host, port))
MAXCLIENTS = 3

sock.listen(MAXCLIENTS)
conn = None

currUser = ''

while (True):
    if (conn is None):
        print('Running on host:', host, 'port: ', port)
        print ('[Waiting for connection...]')
        conn, addr = sock.accept()
        print ('Got connection from', addr)
    else:
        msg = (conn.recv(1024)).decode('utf-8')
        if (msg == ':q'):
            print('Shutting down.')
            conn.sendall(b'Shutting down server.')
            conn.close()
            with open('users.txt', 'w') as outfile:
                #json.dump(users, outfile)
                outfile.write(users)
            break
        else:
            cmd = msg.split()
            ### login funtion
            if (len(cmd) == 3 and cmd[0] == 'login'):
                if currUser != '':
                    response = 'User ' + currUser + ' is already logged in. Please logout first if you wish to login as a differnt user.'
                    conn.sendall(response.encode('utf-8'))
                else:
                    for user in users:
                        if (user['UserID'] == cmd[1] and user['Password'] == cmd[2]):
                            response = 'Server: ' + user['UserID'] + ' joins.'
                            currUser = user['UserID']
                            conn.sendall(response.encode('utf-8'))
                            print(currUser + ' login.')
                            break
                    if (currUser == ''):
                        conn.sendall(b'Incorrect UserID/Password.')
            ### newuser function
            elif (len(cmd) == 3 and cmd[0] == 'newuser'):
                createNewUser = True
                for user in users:
                    if (user['UserID'] == cmd[1]):
                        response = 'Server: ' + user['UserID'] + ' already exists. Please try a different username.'
                        conn.sendall(response.encode('utf-8'))
                        createNewUser = False
                        break
                if (createNewUser == True):
                    if (len(cmd[1]) < 32 and len(cmd[2]) >= 4 and len(cmd[2]) <= 8):
                        users.append({'UserID' : cmd[1], 'Password' : cmd[2]})
                        response = 'User ' + cmd[1] + ' created successfully.'
                        conn.sendall(response.encode('utf-8'))
                    else:
                        conn.sendall(b'The length of the UserID should be less than 32, and the length of the Password should be between 4 and 8 characters.')
            ### send function
            elif (len(cmd) > 0 and cmd[0] == 'send' and cmd[1] != 'all'):
                if (currUser == ''):
                    conn.sendall(b'Denied. Please login in first.')
                else:
                    cmd.remove('send')
                    msg = ' '.join(cmd)
                    msg = currUser + ': ' + msg
                    conn.sendall(msg.encode('utf-8'))
                    print(msg)
            ### send all function
            elif (len(cmd) > 0 and cmd[0] == 'send' and cmd[1] == 'all'):
                    cmd.remove('send')
                    msg = ' '.join(cmd)
                    msg = currUser + ': ' + msg +"sending all"
                    conn.sendall(msg.encode('utf-8'))
                    print(msg)
            elif (len(cmd) > 0 and cmd[0] == 'logout'):
                if (currUser == ''):
                    conn.sendall(b'No user is currently logged in.')
                else:
                    print(currUser + ' logout.')
                    response = 'Server: ' + currUser + ' left.'
                    conn.sendall(response.encode('utf-8'))
                    currUser = ''
                    conn = None
            else:
                conn.sendall(b'Unknown command, or incorrect usage of command. Please try again.')
