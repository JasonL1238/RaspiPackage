import socket
import threading

class RaspiNet:
    def __init__(self):
        self.connections = {}

    def connect_to_device(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 8080))
        self.connections[ip] = s

    def disconnect_device(self, ip):
        self.connections[ip].close()
        del self.connections[ip]

    def send_message(self, message, ip):
        self.connections[ip].sendall(message.encode())

    def receive_message(self, ip):
        return self.connections[ip].recv(1024).decode()

    def send_file(self, file_path, ip):
        with open(file_path, 'rb') as file:
            self.connections[ip].sendfile(file)

    def receive_file(self, destination_path, ip):
        with open(destination_path, 'wb') as file:
            while True:
                data = self.connections[ip].recv(1024)
                if not data:
                    break
                file.write(data)

    def execute_command(self, command, ip):
        self.connections[ip].sendall(command.encode())
        return self.connections[ip].recv(4096).decode()

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

class RaspiServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []

    def handle_client(self, client_socket, address):
        print(f"Connected by {address}")
        while True:
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
        while True:
            client_socket, address = self.server.accept()
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

    def stop(self):
        for client in self.clients:
            client.close()
        self.server.close()
