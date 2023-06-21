import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("Server has been running on {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = self.server_socket.accept()
            print("New client just connected: {}".format(client_address))
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client_socket):
        client_name = client_socket.recv(1024).decode()
        self.nicknames.append(client_name)
        self.clients.append(client_socket)

        self.broadcast("{} joined the chat!".format(client_name).encode())

        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast("{}: {}".format(client_name, message.decode()).encode())
            except:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                client_name = self.nicknames[index]
                self.nicknames.remove(client_name)
                self.broadcast("{} left the chat.".format(client_name).encode())
                break

    def stop(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()

# Run the server
server = Server('localhost', 8000)
server.start()
