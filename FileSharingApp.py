import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
sFile = "Send\Test.txt"
destination = "Recieve\\"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    file = open("data/test.txt", "r")
    data = file.read()

    client.send("test.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 2048


def main():
    print("The revieving side needs to start their program first.")
    print("1. Recieve File")
    print("2. Send File")
    Select()

def Select():
    option = int(input("Are you sending or receiving a file? "))
    if option == 1:
        ReciveFile()
    elif option == 2:
        SendFile()
    else:
        print("Please input valid option. (1 or 2)")
        Select()

def ReciveFile():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Give this to the Sender: {IP}")
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening...")

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] {filename} Recieved")
        file = open(f"Recieve\{filename}", 'w')
        conn.send(f"{filename} received".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] File data received.")
        file.write(data)
        conn.send("File data received.".encode(FORMAT))

        file.close()
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected")

def SendFile():
    Host = input("What is the Host's IP: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    file = open(sFile, "r")
    data = file.read()

    client.send("test.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    file.close()
    client.close()
    

if __name__ == "__main__":
    main()
