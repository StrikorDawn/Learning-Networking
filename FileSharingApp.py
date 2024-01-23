import socket
import tkinter as tk
from tkinter import filedialog
from threading import Thread
# This is to get the file to commit to Github
def receive_file(client_socket, file_name):
    with open(file_name, 'wb') as file:
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            data = client_socket.recv(1024)

def send_file(file_path, server_address):
    with socket.create_connection(server_address) as client_socket:
        file_name = file_path.split("/")[-1]

        # Send the file name
        client_socket.sendall(file_name.encode("utf-8"))

        # Send the file content in chunks
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.sendall(data)
                data = file.read(1024)

    print(f"File '{file_name}' sent successfully.")

def server_thread(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    file_name = client_socket.recv(1024).decode("utf-8")
    print(f"Receiving file: {file_name}")

    receive_file(client_socket, file_name)

    print(f"File received successfully.")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    return server_socket

def on_send_button_click(file_path, server_address):
    Thread(target=lambda: send_file(file_path, server_address)).start()

def on_select_file_button_click(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def main():
    window = tk.Tk()
    window.title("File Sharing GUI")

    host_label = tk.Label(window, text="Server Host:")
    host_label.grid(row=0, column=0)

    host_entry = tk.Entry(window)
    host_entry.grid(row=0, column=1)

    port_label = tk.Label(window, text="Server Port:")
    port_label.grid(row=1, column=0)

    port_entry = tk.Entry(window)
    port_entry.grid(row=1, column=1)

    file_label = tk.Label(window, text="Select File:")
    file_label.grid(row=2, column=0)

    file_entry = tk.Entry(window)
    file_entry.grid(row=2, column=1)

    select_file_button = tk.Button(window, text="Select File", command=lambda: on_select_file_button_click(file_entry))
    select_file_button.grid(row=2, column=2)

    send_button = tk.Button(window, text="Send File", command=lambda: on_send_button_click(file_entry.get(), (host_entry.get(), int(port_entry.get()))))
    send_button.grid(row=3, column=0, columnspan=3)

    window.mainloop()

if __name__ == "__main__":
    server_socket = start_server("localhost", 12345)
    Thread(target=lambda: server_thread(server_socket)).start()
    main()
