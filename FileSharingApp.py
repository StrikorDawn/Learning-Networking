import socket
# Initialization Variables
IP = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (IP, PORT)
FORMAT = "utf-8"
#Size limit for the files being transered
SIZE = 1024
# Variables for Configuration
# Will utilize them more in the future for GUI implimentation.
sFile = "Send\Test.txt"
destination = "Recieve\\"

# Start up navigation, user selectes if they are hosting or connecting to the other program.
def main():
    option = 0
    # Allows for multiple files to be sent without rebooting the program multiple times
    while option != 3:
        # Creates a break to make the terminal more readable
        print("")
        # Display options
        print("What would you like to do?")
        print("1. Recieve File")
        print("2. Send File")
        print("3. Quit")
        option = Select()
        if option == 1:
            ReciveFile()
        elif option == 2:
            SendFile()
        elif option == 3:
            # Makes it so the program finishes correctly without prompting the user with an error
            pass
        else:
            print("Please input valid option. (1, 2 or 3)")
            Select()

# Takes the input from the user and call the appropriate funcion.
def Select():
    option = int(input("> "))
    return option 
    
def ReciveFile():
    print("[STARTING] Server is starting...")
    # Initiates the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Displays the users IP so they can share it to the sender.
    print(f"Give this to the Sender: {IP}")
    # Opens port for file traffic
    server.bind(ADDR)
    # Listens for incoming connection attempts
    server.listen()
    print("[LISTENING] Server is listening...")\
    # Creates Exit var for file sending
  
    # Accepts incomming connection requests over the specified port
    conn, addr = server.accept()
    # Displays to the user the IP of the connecting computer.
    print(f"[NEW CONNECTION] {addr} connected.")
    # saves the file infromation to a variable to be writen to the specified location.
    filename = conn.recv(SIZE).decode(FORMAT)
    print(f"[RECV] {filename} Recieved")
    file = open(f"Recieve\{filename}", 'w')
    # Returns that the File has been recieved
    conn.send(f"{filename} received".encode(FORMAT))
    # Retrieves the information that is to be written to the file
    data = conn.recv(SIZE).decode(FORMAT)
    print(f"[RECV] File data received.")
    # Writes the text to the file that was sent
    file.write(data)
    # Retruns to the other user that the file data has been written and recieved.
    conn.send("File data received.".encode(FORMAT))
    # Closes the transfed file
    file.close()
    # Disconnects the other user from the Host
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected")


def SendFile():
    # User inputs Host IP recived from Host.
    Host = input("What is the Host's IP: ")
    # Opens Server Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connects to the provided IP if accepted
    client.connect(ADDR)
    # Reads the file that has been selected for sending
    file = open(sFile, "r")
    # Reads the contents of the file for sending
    data = file.read()
    # Sends File
    client.send("test.txt".encode(FORMAT))
    # Displays back to the user if the file was recived
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    # Sends file data
    client.send(data.encode(FORMAT))
    # Displays Message from host that file has been recieved.
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    # Closes File
    file.close()
    # Closes Connection and port for file sharing
    client.close()

if __name__ == "__main__":
    main()