import socket
import psutil
import json

HOST = "0.0.0.0"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on on {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print(f"Connected to {addr}")
    request = client_socket.recv(1024).decode('utf-8')
    if request == "get_processes":
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            processes.append(proc.info["name"])
        response = json.dumps(processes)
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()