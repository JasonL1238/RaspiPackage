#poetry run python -m unittest tests/test_core.py
import unittest
from raspinet.core import RaspiNet, RaspiServer
import threading
import socket
import time

class TestCore(unittest.TestCase):
    def setUp(self):
        self.core = RaspiNet()
        self.server = None
        self.server_thread = None

    def start_mock_server(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()

    def accept_connections(self):
        while True:
            try:
                client_socket, _ = self.server.accept()
                client_socket.sendall(b"Hello")
                client_socket.close()
            except OSError:
                break

    def tearDown(self):
        if self.server:
            self.server.close()
        if self.server_thread:
            self.server_thread.join()

    def test_connect_to_device(self):
        port = 8081
        self.start_mock_server(port)
        time.sleep(1)  # Ensure server has enough time to start
        self.core.connect_to_device('127.0.0.1', port)
        self.assertIn(('127.0.0.1', port), self.core.connections)

    def test_disconnect_device(self):
        port = 8082
        self.start_mock_server(port)
        time.sleep(1)  # Ensure server has enough time to start
        self.core.connect_to_device('127.0.0.1', port)
        self.core.disconnect_device('127.0.0.1', port)
        self.assertNotIn(('127.0.0.1', port), self.core.connections)

    def test_send_receive_message(self):
        port = 8083
        self.start_mock_server(port)
        time.sleep(1)  # Ensure server has enough time to start
        self.core.connect_to_device('127.0.0.1', port)
        self.core.send_message("Hello", '127.0.0.1', port)
        response = self.core.receive_message('127.0.0.1', port)
        self.assertEqual(response, "Hello")

if __name__ == '__main__':
    unittest.main()
