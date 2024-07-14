from raspinet.file_service import FileServer
import time

if __name__ == "__main__":
    server = FileServer(host='0.0.0.0', port=8080)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
