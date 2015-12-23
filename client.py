import select
import socket
import sys
import json
import getch    #https://pypi.python.org/pypi/getch

#Auth
isValidated = False
while not isValidated:
    username = raw_input('Enter Username : ')
    password = raw_input('Enter Password : ')
    #Create the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.connect(('localhost', 8888))

    server_socket.send(json.dumps({"username":username,"password":password}))
    data = server_socket.recv(1024)
    if data == "AuthSuccess":
        isValidated=True
        data = ''
        msg = ''
        print '\n Welcome... '
        read_list = [sys.stdin, server_socket]
        while True:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                #print read_list
                if s==server_socket:
                    data = s.recv(1024)
                    sys.stdout.write(data)
                    sys.stdout.flush()
                else:
                    msg = sys.stdin.readline()
                    #Quit chat room
                    if msg[:-1] == "exit":
                        print '\nExiting the chat room.. Bye.. '
                        exit(0)
                        break
                    server_socket.send(msg)
                    #
                    sys.stdout.write('\033[A')
                    sys.stdout.write(username + ' : '+msg)
                    sys.stdout.flush() 
    
    else:
        print data
    server_socket.close()