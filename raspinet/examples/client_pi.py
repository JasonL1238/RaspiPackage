#poetry run python examples/client_pi.py 127.0.0.1
from raspinet.chat import start_chat_client
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client_example.py [server_ip]")
        sys.exit(1)

    server_ip = sys.argv[1]
    client = start_chat_client(server_ip)

    while True:
        message = input("")
        client.send_message(message)
