import threading
import time
from raspinet.chat import start_chat_server, start_chat_client

def run_server():
    server = start_chat_server()

def run_client(server_ip, client_id):
    client = start_chat_client(server_ip)
    while True:
        message = f"Message from client {client_id}"
        client.send_message(message)
        time.sleep(1)  

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    time.sleep(2)

    server_ip = '127.0.0.1'

    client_threads = []
    for i in range(3): 
        client_thread = threading.Thread(target=run_client, args=(server_ip, i + 1))
        client_threads.append(client_thread)
        client_thread.start()

    time.sleep(10)  

    for client_thread in client_threads:
        client_thread.join()

   
