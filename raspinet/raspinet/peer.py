from .core import RaspiNet, RaspiServer
import threading

class Peer:
    def __init__(self, host_ip, port=8080):
        self.network = RaspiNet()
        self.server = RaspiServer(host=host_ip, port=port)
        self.connections = {}  # Dictionary to store connections by (ip, port)
        threading.Thread(target=self.start_server).start()

    def start_server(self):
        print(f"Peer started on {self.server.host}:{self.server.port}")
        while True:
            client_socket, address = self.server.server.accept()
            self.connections[address] = client_socket
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

    def handle_client(self, client_socket, address):
        print(f"Connected by {address}")
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                formatted_message = f"Message from {address}: {message}"
                print(formatted_message)
            except:
                break
        client_socket.close()
        del self.connections[address]
        print(f"Connection with {address} closed")

    def connect_to_peer(self, peer_ip, peer_port):
        self.network.connect_to_device(peer_ip, peer_port)
        self.connections[(peer_ip, peer_port)] = self.network.connections[(peer_ip, peer_port)]
        threading.Thread(target=self.receive_messages_from_peer, args=(peer_ip, peer_port)).start()

    def send_message_to_peer(self, message, peer_ip, peer_port):
        formatted_message = f"Message from {self.network.get_local_ip()}: {message}"
        self.network.send_message(formatted_message, peer_ip, peer_port)

    def receive_messages_from_peer(self, peer_ip, peer_port):
        while True:
            try:
                message = self.network.receive_message(peer_ip, peer_port)
                if message:
                    formatted_message = f"Message from {peer_ip}:{peer_port}: {message}"
                    print(formatted_message)
            except:
                print(f"Connection with {peer_ip}:{peer_port} closed")
                self.network.disconnect_device(peer_ip, peer_port)
                del self.connections[(peer_ip, peer_port)]
                break
