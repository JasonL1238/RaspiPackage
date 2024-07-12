from raspinet.peer import Peer
import time
import threading

def run_peer1():
    peer1 = Peer('0.0.0.0', 8080) 
    time.sleep(20)  
    peer1.connect_to_peer('127.0.0.1', 8081)  
    time.sleep(1)

    def send_messages():
        while True:
            message = input("")
            peer1.send_message_to_peer(message, '127.0.0.1', 8081)

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

if __name__ == "__main__":
    run_peer1()
