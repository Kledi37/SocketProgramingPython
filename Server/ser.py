#KLEARD MAMA
#ser.py (SERVER)
import socket
import threading
import os

HEADER = 64
PORT = 5050
BUFFER_SIZE = 1024
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg_split = msg.split(" ")
            print(f"[{addr}] {msg}")

            if msg == DISCONNECT_MESSAGE:
                connected = False

            # HANDLE Help Command
            elif msg == "help":
                conn.send(
                    "Possible Commands:\n put filename\n get filename\n change oldfilename newfilename \n help\n bye".encode(
                        FORMAT))
                continue


            # HANDLE Put Command
            elif msg_split[0] == "p":
                conn.send("[File was put]".encode(FORMAT))
                filename = msg_split[1]
                with open(filename, "wb") as f:  #Creates new file with the name received from the client
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        f.write(data)               #Writes the data into the file
                        if data==b" "*len(data):    #Check if the all the file data has been receive
                            break                   #So that we can break out of the while loop
                continue

            # HANDLE Change Command
            elif msg_split[0] == "c":
                if os.path.exists(msg_split[1]):    #Check if oldFile exists
                    os.rename(msg_split[1],msg_split[2])    #Rename oldFile to NewFile
                    conn.send("[Name was successfully changed]".encode(FORMAT))
                else:
                    conn.send("[Could not change file name because file was not found]".encode(FORMAT))
                continue

            # HANDLE Get Command
            elif msg_split[0] == "g":
                nameOfFile=msg_split[1]
                with open(nameOfFile, "rb") as fi:  #Read from file
                    bytesRead = fi.read(BUFFER_SIZE)
                    conn.send("[Get File]".encode(FORMAT))
                    conn.sendall(bytesRead)
                    while True:
                        #Check if we have read all data from file
                        if not bytesRead:
                            endByte = b" " * 1024
                            conn.send(endByte)
                            break
                            #Send empty data which tells the client that the data has ended
                            #Then brake out of the while loop
                        bytesRead = fi.read(BUFFER_SIZE)
                        conn.sendall(bytesRead)
                continue
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
