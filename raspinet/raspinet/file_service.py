from raspinet.core import RaspiNet, RaspiServer
import os

class FileServer(RaspiServer):
    def __init__(self, host='0.0.0.0', port=8080):
        super().__init__(host, port)
        self.start(self.handle_client)

    def handle_client(self, client_socket, address):
        print(f"Connected by {address}")
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                command, *args = message.split()
                if command == 'UPLOAD':
                    file_name = args[0]
                    self.receive_file(client_socket, file_name)
                elif command == 'DOWNLOAD':
                    file_name = args[0]
                    self.send_file(client_socket, file_name)
                elif command == 'LIST':
                    self.list_files(client_socket)
                else:
                    client_socket.sendall(b'ERROR: Unknown command')
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()
        print(f"Connection with {address} closed")

    def receive_file(self, client_socket, file_name):
        with open(file_name, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if data.endswith(b'EOF'):
                    file.write(data[:-3])
                    break
                file.write(data)

    def send_file(self, client_socket, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                while chunk := file.read(1024):
                    client_socket.sendall(chunk)
            client_socket.sendall(b'EOF')
        else:
            client_socket.sendall(b'ERROR: File not found')

    def list_files(self, client_socket):
        files = os.listdir('.')
        file_list = '\n'.join(files)
        client_socket.sendall(file_list.encode())

class FileClient:
    def __init__(self, server_ip, port=8080):
        self.network = RaspiNet()
        self.server_ip = server_ip
        self.port = port
        self.network.connect_to_device(server_ip, port)

    def upload_file(self, file_path):
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            self.network.send_message(f'UPLOAD {file_name}', self.server_ip, self.port)
            self.network.send_file(file_path, self.server_ip, self.port)
        else:
            print("ERROR: File not found")

    def download_file(self, file_name, destination_path):
        self.network.send_message(f'DOWNLOAD {file_name}', self.server_ip, self.port)
        self.network.receive_file(destination_path, self.server_ip, self.port)

    def list_files(self):
        self.network.send_message('LIST', self.server_ip, self.port)
        files = self.network.receive_message(self.server_ip, self.port)
        print("Files on server:")
        print(files)
