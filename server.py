import select
import socket
import json

#connectedUsers
connectedUsers = {}
#User Details
userDetails = {}
#Read list for select
read_list = []
#User cred to validate
with open('./users.json') as data_file:
    print data_file
    users = json.load(data_file)

#Offline Message Store
offlineMessages = {}

def initiateOfflineMessages():
    global offlineMessages
    for i in users:
        offlineMessages[i] = ''
        

def addToOfflineMessages(msg):
    global offlineMessages
    for user in users:
        if not user in connectedUsers:
            offlineMessages[user] += msg


def retrieveOfflineMessages(user):
    global offlineMessages
    msg = offlineMessages[user]
    offlineMessages[user] = ''
    return msg


def sendToUser(msg,sender,user):
    msg = userDetails[sender]['name'] + ' : '+msg
    for i in userDetails:
        if userDetails[i]['name']==user:
            if user in connectedUsers:
                i.send(msg.encode('utf-8'))
            else:
                global offlineMessages
                offlineMessages[user] += data
            
    
def sendAll(msg,sender):
    msg = userDetails[sender]['name'] + ' : '+msg
    for i in read_list:
        if not i is  server_socket and not i is sender:
            i.send(msg.encode('utf-8'))
    addToOfflineMessages(msg)


def addUserDetails(address,name):
    global userDetails, connectedUsers
    connectedUsers[name] = 1
    userDetails[client_socket] = {'name':name,'address':address}
            

def validateUser(data,client_socket):
    #Validate for username and password
    if(data['username'] in users and data['password']==users[data['username']]):
        if data['username'] in connectedUsers:
            #InvalidUser
            client_socket.send('\n    User Already Logged in..Login Failed.\n')
            client_socket.close()
        else:
            #Valid user
            client_socket.send('AuthSuccess')
            #Add to user Details
            addUserDetails(address,data['username'])

            #Add to connected List
            global read_list
            read_list.append(client_socket)
            
            #Send offline messages
            client_socket.send(retrieveOfflineMessages(data['username']))
    else:
        #InvalidUser
        client_socket.send('\n    Invalid Credentials\n')
        client_socket.close()



initiateOfflineMessages()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 8888))
server_socket.listen(5)
print "Chat Server Started at 8888"

read_list = [server_socket]
while True:
    readable, writable, errored = select.select(read_list, [], [])
    for s in readable:
        #print read_list
        if s is server_socket:
            client_socket, address = server_socket.accept()
            print "Connection from", address
            
            #Get username and password
            data = client_socket.recv(1024)
            data = json.loads(data)        
            #Validate user and do the corresponding task
            validateUser(data,client_socket)
        else:
            data = s.recv(1024)
            print data
            if data:
                #print 'Broadcasting'
                #s.send(data)
                x = data.split()[0] if len(data.split())>0 else ' '
                if x[0]=='@' and len(x)>1 and x[1:] in users:
                    print 'Message from ',userDetails[s]['name'],' to ',x[1:]
                    sendToUser(' '.join(data.split()[1:]),s, x[1:])
                else:
                    print 'Message to All'
                    sendAll(data,s)
            else:
                print 'Closing socket ',s 
                s.close()
                del connectedUsers[userDetails[s]['name']]
                del userDetails[s]
                read_list.remove(s)