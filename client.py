import socket
import threading
import random

# defined/given info
print("Enter IP, could be 127.0.0.1 :)")
IP = input('')
print("Enter PORT Number")
PORT = int(input())
ADDR = (IP, PORT)
print(f"ADDR: {ADDR}")

BUFF = 1024
ENC = 'utf-8'

# The code have different bots so the client has to define him/her self one of those
while True:
    print("Choose one of bots below:\n 1. John \n 2. Milen \n 3. Maria \n 4. Eminem")
    msg = input()
    if "1" in msg or "John" in msg:
        name = "John"
        break
    elif "2" in msg or "Milen" in msg:
        name = "Milen"
        break
    elif "3" in msg or "Maria" in msg:
        name = "Maria"
        break
    elif "4" in msg or "Eminem" in msg:
        name = "Eminem"
        break

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(ADDR)
except:
    print("Connection failed")

# list actions the choosen bot have used
used_actions = []


# 4 bot functions
# Bot John
def bot(msg):
    if name == "John":
        # here decide we that we want a good bot or a bad bot where the bot response to the user in different ways
        yes_things = ["read", "write", "play", "train"]
        no_things = ["fight", "hug", "yell", "complain", "cry"]

        # extracting the suggested action from the received message in the form of a list
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        # when one yes action is used, it will be stored as used and return the sentence I want
        if yes_action:
            if yes_action[0] in used_actions:
                return "yes, im ready for thattttt."

            used_actions.append(yes_action[0])
            return f"I'm ready for some {yes_action[0]}ing."

        # now the same for no action
        elif no_action:
            if no_action[0] in used_actions:
                return "come on im waiting to hear something new"
            used_actions.append(no_action[0])
            return f"What? I don't want to {no_action[0]}."

        # if there is no action so:
        return "Have nothing to say!"

    # Bot Milen
    elif name == "Milen":
        # yes and no things/actions for Milen
        yes_things = ["fight", "punch", "yell", "complain", "cry"]
        no_things = ["dance", "hug", "play", "read", "run", "communicate", "talk"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            if yes_action[0] in used_actions:
                return "No word to say"
            used_actions.append(yes_action[0])
            return f"Yes! who doesn't want {yes_action[0]}ing."
        elif no_action:
            if no_action[0] in used_actions:
                return "No!!!"
            used_actions.append(no_action[0])
            return f"Not sure about {no_action[0]}ing."
        return "Boring!!!"

    # Bot Maria
    elif name == "Maria":
        yes_things = ["yell", "hug", "draw", "work"]
        no_things = ["fight", "steal", "yell", "complain"]
        yes_action = [string for string in yes_things if string in msg]
        no_action = [string for string in no_things if string in msg]

        if yes_action:
            if yes_action[0] in used_actions:
                return "can we change the subject?!!"
            used_actions.append(yes_action[0])
            return f"waiting for "
        elif no_action:
            if no_action[0] in used_actions:
                return "pufff."

            # this bot can reply with a suggestion
            used_actions.append(no_action[0])
            suggestion = random.choice(yes_things)
            return f"That no fun, what about {suggestion}ing?"
        return "cool."

    # Bot Eminem
    else:
        things = ["sing", "kiss", "play", "work", "dance", "shoot", "yell", "complain", "sleep", "code", ]
        action = [string for string in things if string in msg]

        if action:
            if action[0] in used_actions:
                return "Yes! I'm in."
            used_actions.append(action[0])
            return f"I think {action[0]}ing sounds great!"
        return "I said I'm in."


# takes care about quit function and try to send inputs
def send():
    while True:
        try:
            msg = f"{name} : {input()}"

            # if user want to quit then will this if sentence come in th road and put the user on break
            if msg == f"{name} : quit":
                # encoding
                s.send(msg.encode(ENC))
                break
            else:
                s.send(msg.encode(ENC))
        except:
            print("ERROR: Can't send, the connection going to be closed!!! Try again later.")
            s.close()
            break


# Now we want to loop over received messages (there might be more than one) and print them
def rece():
    while True:
        try:
            msg = s.recv(BUFF).decode(ENC)

            # quit function, checking for any request about quit
            if msg == "quit":
                s.close()
                break

            # function about the server is asking for your name
            elif msg == "NAME?":
                s.send(name.encode(ENC))

            # checking the message from host and then the bot going to make an action
            elif "HOST : " in msg:
                print(msg)
                message = bot(msg)
                if message:
                    print(message)
                    s.send(f"{name} : {message}".encode(ENC))

            # printing message from clients
            else:
                print(msg)

        except:
            # exception if the connection is broken
            print("ERROR: Disconnect")
            s.close()
            break


# threading start function and it's ready for whole script
th1 = threading.Thread(target=send)
th1.start()

# the same for receive function
th2 = threading.Thread(target=rece)
th2.start()

""" so now with all of our scripts we do have many function as send and receive which can be called/seen as chat
but we do have bots where we get auto response from those so, its not just a chat room its a chatbot room with
 exciting function as listing clients and kick"""
