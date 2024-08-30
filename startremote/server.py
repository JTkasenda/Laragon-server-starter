import socket

# Set up the server to send commands
def start_server(host, port, command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(command.encode('utf-8'))
            response = conn.recv(1024)
            print(f"Response: {response.decode('utf-8')}")

if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all interfaces
    port = 9999       # Port to listen on
    command = "notepad.exe"  # Command to execute on the client

    start_server(host, port, command)
