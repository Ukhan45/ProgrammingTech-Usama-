import threading
import socket
import argparse
import os

class ChatServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")

            client_handler = ClientHandler(client_socket, client_address, self)
            client_handler.start()

            self.connections.append(client_handler)
            print(f"Connection ready for {client_address}")

    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.address != source:
                connection.send_message(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.address = client_address
        self.server = server

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"{self.address} says: {message}")
                    self.server.broadcast(message, self.address)
                else:
                    print(f"{self.address} has disconnected")
                    self.client_socket.close()
                    self.server.remove_connection(self)
                    return
            except ConnectionResetError:
                print(f"{self.address} connection reset")
                self.client_socket.close()
                self.server.remove_connection(self)
                return

    def send_message(self, message):
        self.client_socket.sendall(message.encode('utf-8'))

def shutdown_server(server):
    while True:
        command = input("")
        if command.lower() == "quit":
            print("Shutting down server...")
            for connection in server.connections:
                connection.client_socket.close()
            os._exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument('host', help='Server host address')
    parser.add_argument('-p', '--port', type=int, default=12345, help='Server port (default 12345)')

    args = parser.parse_args()

    server = ChatServer(args.host, args.port)
    server.start()

    shutdown_thread = threading.Thread(target=shutdown_server, args=(server,))
    shutdown_thread.start()
