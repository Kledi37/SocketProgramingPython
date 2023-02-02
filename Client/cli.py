#KLEARD MAMA
#cli.py (CLIENT)
import socket
import os

HEADER = 64
PORT = 5050
BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#Send Function
#First sends the length of the message in a header of size 64
#Then sends the message
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while (1):
    command = input("Input Command:")
    commandSplit=command.split(" ")
    filename=""

    #HANDLE Bye Command
    if (command.lower() == "bye"):
        send(DISCONNECT_MESSAGE)
        client.close()
        exit(0)

    #HANDLE Help Command
    elif (command.lower() == "help"):
        send("help")

    #HANDLE Put Command
    elif (commandSplit[0].lower()=="put"):
        filename=commandSplit[1]
        if(os.path.exists(filename)):   #Check if file exists before sending it to server
            putMessage="p "+filename
            send(putMessage)    #Sends Put Message
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)    #Reads and sends file data in chunks of BUFFER_SIZE(1024)
                    client.sendall(bytes_read)
                    if not bytes_read:
                        endByte=b" "*1024   #Sends empty data to signify that all the data has been sent
                        client.send(endByte)
                        break
        else:
            print("File does not exist try again")

    #HANDLE Change Command
    elif (commandSplit[0].lower()=="change"):
        changeMessage="c "+commandSplit[1]+" "+commandSplit[2]
        send(changeMessage)

    #HANDLE Get Command
    elif (commandSplit[0].lower()=="get"):
        getMessage="g "+commandSplit[1]
        send(getMessage)    #Sends Get Message and waits for the data from the file
        with open(commandSplit[1], "wb") as g:
            while True:
                data = client.recv(BUFFER_SIZE)
                g.write(data)
                if data == b" " * len(data):    #Checks if all data has been received
                    break
            send(" ")