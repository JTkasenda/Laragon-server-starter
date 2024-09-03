import socket
import subprocess
import sys
import os

def start_client(server_ip, server_port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, server_port))
                while True:
                    command = s.recv(1024).decode('utf-8')
                    if command:
                        try:
                            if "mysql" in command.lower():
                                # Start MySQL in a detached mode in another console
                                subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
                                s.sendall(b"MySQL started in detached mode")
                            else:
                                # Start Apache or any other command in the current console
                                subprocess.run(command, shell=True, check=True)
                                s.sendall(b"Process started successfully")
                        except subprocess.CalledProcessError as e:
                            error_msg = f"Command failed with return code {e.returncode}: {str(e)}"
                            s.sendall(error_msg.encode('utf-8'))
                        except Exception as e:
                            error_msg = f"Error: {str(e)}"
                            s.sendall(error_msg.encode('utf-8'))
        except Exception as e:
            print(f"Connection failed: {e}. Retrying...")
            continue

if __name__ == "__main__":
    server_ip = "192.168.1.64"  # Replace with your server's IP address
    server_port = 9999          # Replace with your server's port
    start_client(server_ip, server_port)
