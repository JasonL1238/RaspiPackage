import socket
import threading

class RaspiNet:
    def __init__(self):
        self.connections = {}

    def connect_to_device(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        self.connections[(ip, port)] = s

    def disconnect_device(self, ip, port):
        if (ip, port) in self.connections:
            self.connections[(ip, port)].close()
            del self.connections[(ip, port)]

    def send_message(self, message, ip, port):
        if (ip, port) in self.connections:
            self.connections[(ip, port)].sendall(message.encode())

    def receive_message(self, ip, port):
        if (ip, port) in self.connections:
            return self.connections[(ip, port)].recv(1024).decode()
        return None

    def send_file(self, file_path, ip, port):
        if (ip, port) in self.connections:
            with open(file_path, 'rb') as file:
                while chunk := file.read(1024):
                    self.connections[(ip, port)].sendall(chunk)
            self.connections[(ip, port)].sendall(b'EOF')

    def receive_file(self, destination_path, ip, port):
        if (ip, port) in self.connections:
            with open(destination_path, 'wb') as file:
                while True:
                    data = self.connections[(ip, port)].recv(1024)
                    if data.endswith(b'EOF'):
                        file.write(data[:-3])
                        break
                    file.write(data)

class RaspiServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.stop_event = threading.Event()

    def start(self, handle_client):
        print(f"Server listening on {self.host}:{self.port}")
        while not self.stop_event.is_set():
            client_socket, address = self.server.accept()
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()

    def stop(self):
        self.stop_event.set()
        for client in self.clients:
            client.close()
        self.server.close()
