import socket
import threading
import os

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
                self.connections[(ip, port)].sendfile(file)

    def receive_file(self, destination_path, ip, port):
        if (ip, port) in self.connections:
            with open(destination_path, 'wb') as file:
                while True:
                    data = self.connections[(ip, port)].recv(1024)
                    if not data:
                        break
                    file.write(data)

    def execute_command(self, command, ip, port):
        if (ip, port) in self.connections:
            self.connections[(ip, port)].sendall(command.encode())
            return self.connections[(ip, port)].recv(4096).decode()
        return None

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def discover_devices(self):
        # Placeholder implementation for discovering devices
        return [self.get_local_ip()]

class RaspiServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.stop_event = threading.Event()

    def handle_client(self, client_socket, address):
        print(f"Connected by {address}")
        while not self.stop_event.is_set():
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                client_socket.sendall(message)
            except:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        print(f"Connection with {address} closed")

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")
        while not self.stop_event.is_set():
            client_socket, address = self.server.accept()
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

    def stop(self):
        self.stop_event.set()
        for client in self.clients:
            client.close()
        self.server.close()
