import socket
import threading

# defined/given info
# this going to be our ip as like host ip or your pc ip as easy declaration
IP = '127.0.0.1'
# portnr going to be used as like a password/key to our chat so if the client server write it fail it going to not work
PORT = 10365
ADDR = (IP, PORT)

BUFF = 1024
ENC = 'utf-8'

""" cl or c stands for client, msg stands for message"""

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding IP and Port
s.bind(ADDR)

# This makes server listen to new connections, can be limited to
s.listen()

# some arrays that store info and will be used later
clients = []
addresses = []
names = []


# lists address and name of all connected clients
def allclients():
    cllist = f"Number of clients: {len(clients)}"
    for cl in clients:
        # gets the address and name of the clients
        index = clients.index(cl)
        name = names[index]
        addr = addresses[index]
        cllist += f"\n{addr} : {name}"
    return cllist


# kick function
def quit(cl):
    try:
        # defining everything for input and outputs for this function
        index = clients.index(cl)
        clients.remove(cl)
        cl.close()
        name = names[index]
        addr = addresses[index]

        # print the message with detail about diconnecting
        dcmsg = f"[DISCONNECTED] {name}"
        print(dcmsg)
        broadcast(cl, dcmsg)

        # removing
        names.remove(name)
        addresses.remove(addr)
    except:
        # if a client has been removed or doesn't exist
        # then will this message be shown
        print("It's done. KICKED!!!")


# host ip inform/send
def send():
    while True:
        msg = input()

        # command to list all clients which is defind in line 31
        if msg.startswith("/clients"):
            print(allclients())

        # command to kick a clien which is defind in line 43
        elif msg.startswith("/kick"):
            # get kicknames
            kicknames = [string for string in names if string in msg]
            for kickname in kicknames:
                index = names.index(kickname)
                c = clients[index]
                quit(c)
        else:
            # else will be send message from host side >>
            message = "HOST : " + msg
            for c in clients:
                c.send(message.encode(ENC))


# broadcast
def broadcast(c, msg):
    for client in clients:
        # the client who sends the message will not receive on his display
        if c != client:
            client.send(msg.encode(ENC))


# function to handle the clients
def run(c):
    while True:
        try:
            # get message from client and will be decoded
            msg = c.recv(BUFF).decode(ENC)

            # get the name of client
            index = clients.index(c)
            name = names[index]

            # Checking for disconnecting/kick
            if msg == f"{name} : quit":
                c.send("quit".encode(ENC))
                quit(c)
                break

            # Checking for command of listing every clients
            elif msg == f"{name} : /clients":
                c.send(allclients().encode(ENC))

            # prints and broadcasts the messages
            else:
                print(msg)
                broadcast(c, msg)
        except:
            # if its some issues the client will be closed
            # it can be the user have used ctrl + c or have just closed the window
            quit(c)
            break


# it's a function which can be seen as like an entrance for clients where they can just join the server
def start():
    while True:
        # accepting first the client
        # the send & recieve string
        c, addr = s.accept()
        c.send("NAME?".encode(ENC))
        name = c.recv(BUFF).decode(ENC)
        names.append(name)

        # listing
        clients.append(c)
        addresses.append(addr)

        # printing details of new clients
        print(f"{name} JOINED")
        broadcast(c, f"{name} JOINED")
        c.send("[CONNECTED]".encode(ENC))

        # a new thread for run function where It's needed to handle clients
        th1 = threading.Thread(target=run, args=(c,))
        th1.start()


# threading start function and it's ready for whole script
th2 = threading.Thread(target=send)
th2.start()

# server is listening
print(f"SERVER IS LISTENING ON {ADDR}")
# running the start function
start()
