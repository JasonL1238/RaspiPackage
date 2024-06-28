from .core import RaspiNet, RaspiServer
import threading

class ChatServer:
    def __init__(self, port=8080):
        self.server = RaspiServer(port=port)

    def handle_client(self, client_socket, address):
        print(f"Connected by {address}")
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                formatted_message = f"{address}: {message}"
                print(f"Broadcasting message: {formatted_message}")
                self.broadcast_message(formatted_message, client_socket)
            except:
                break
        client_socket.close()
        print(f"Connection with {address} closed")

    def broadcast_message(self, message, sender_socket):
        for client in self.server.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode())
                except:
                    client.close()
                    self.server.clients.remove(client)

    def start(self):
        print(f"Chat server started on port {self.server.port}")
        while True:
            client_socket, address = self.server.server.accept()
            self.server.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

class ChatClient:
    def __init__(self, server_ip, port=8080):
        self.network = RaspiNet()
        self.server_ip = server_ip
        self.port = port
        self.network.connect_to_device(server_ip, port)
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                message = self.network.receive_message(self.server_ip, self.port)
                if message:
                    print(message)
            except:
                print("Connection closed")
                self.network.disconnect_device(self.server_ip, self.port)
                break

    def send_message(self, message):
        formatted_message = f"{self.network.get_local_ip()}: {message}"
        self.network.send_message(formatted_message, self.server_ip, self.port)

def start_chat_server():
    server = ChatServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    return server

def start_chat_client(server_ip):
    client = ChatClient(server_ip)
    return client
