from raspinet.file_service import FileClient
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_file_client.py <server_ip>")
        sys.exit(1)

    server_ip = sys.argv[1]
    client = FileClient(server_ip=server_ip, port=8080)

    while True:
        command = input("Enter command (CREATE_UPLOAD/RETRIEVE/LIST/EXIT): ").strip().upper()
        if command == 'CREATE_UPLOAD':
            file_name = input("Enter the name of the file to create and upload: ").strip()
            file_content = input("Enter the content of the file: ").strip()
            # Create the file
            with open(file_name, 'w') as file:
                file.write(file_content)
            # Upload the file
            client.upload_file(file_name)
        elif command == 'RETRIEVE':
            file_name = input("Enter the name of the file to retrieve: ").strip()
            destination_path = input("Enter the destination path: ").strip()
            client.download_file(file_name, destination_path)
        elif command == 'LIST':
            client.list_files()
        elif command == 'EXIT':
            break
        else:
            print("Unknown command. Please try again.")