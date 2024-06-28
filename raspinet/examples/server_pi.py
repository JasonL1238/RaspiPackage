#poetry run python examples/server_pi.py

from raspinet.chat import start_chat_server

if __name__ == "__main__":
    server = start_chat_server()
