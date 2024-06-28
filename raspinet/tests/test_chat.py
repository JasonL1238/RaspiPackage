import unittest
from chat import ChatServer, ChatClient
import threading
import time

class TestChat(unittest.TestCase):
    def test_server_client_communication(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()
        time.sleep(1)  # Give server time to start

        client1 = ChatClient('127.0.0.1')
        client2 = ChatClient('127.0.0.1')

        client1.send_message("Hello from Client 1")
        time.sleep(1)  

        client2.send_message("Hello from Client 2")
        time.sleep(1)  

    def run_server(self):
        server = ChatServer()
        server.start()

if __name__ == '__main__':
    unittest.main()
