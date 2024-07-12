from raspinet.peer import Peer
import time
import threading

def run_peer2():
    peer2 = Peer('0.0.0.0', 8081)  # Start peer2 on port 8081
    time.sleep(20)  # Wait for peer1 to connect
    peer2.connect_to_peer('127.0.0.1', 8080)  # Connect peer2 to peer1
    time.sleep(1)

    def send_messages():
        while True:
            message = input("")
            peer2.send_message_to_peer(message, '127.0.0.1', 8080)

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

if __name__ == "__main__":
    run_peer2()
