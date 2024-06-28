import unittest
from core import Core
import threading
import socket

class TestCore(unittest.TestCase):
    def setUp(self):
        self.core = Core()

    def test_discover_devices(self):
        devices = self.core.discover_devices()
        self.assertIn('127.0.0.1', devices)

    def test_connect_to_device(self):
        server_thread = threading.Thread(target=self.start_mock_server)
        server_thread.start()
        client_socket = self.core.connect_to_device('127.0.0.1')
        self.assertIsNotNone(client_socket)

    def start_mock_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8080))
        server_socket.listen(5)
        server_socket.accept()

    def test_send_receive_message(self):
        server_thread = threading.Thread(target=self.start_mock_server)
        server_thread.start()
        client_socket = self.core.connect_to_device('127.0.0.1')
        self.core.send_message(client_socket, "Hello")
        self.assertEqual(self.core.receive_message(client_socket), "Hello")

    def test_disconnect_device(self):
        server_thread = threading.Thread(target=self.start_mock_server)
        server_thread.start()
        client_socket = self.core.connect_to_device('127.0.0.1')
        self.core.disconnect_device(client_socket)
        self.assertNotIn(client_socket, self.core.devices)

if __name__ == '__main__':
    unittest.main()
