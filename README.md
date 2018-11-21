# CS4850 Computer Networks 

### Lab 3 - Chatroom Version 2

This program implements the client side of the CS4850 Lab 3 Version 2 (BONUS). 
An executable server.py and client.py is in the folder
Usage: 
 
$python server.py
 
$python client.py

Available commands:

commands|function |
---|---|
login *username* *password*|login to the server
newuser *username* *password*|create a new user account
send all *message*|send a message to all users
send *username* *message*|whisper a message to another user
send *message*|send a message to the server(lab version 1)
who|list all users on the server
logout|logout and exit the program
quit|quit the program
help|display this menu.

The program will attempt to connect to the server program on the current host.

If the server is currently handling the maximum amount of clients (in this lab, 3), the client
will be blocked by the server until a connection is made available. You may type "quit"
to exit the program at any time.
