import socket
import threading

# Function to handle each client connection
def handle_client(conn, addr, command):
    print(f"New connection from {addr}")
    try:
        while True:
            # Get command from the user
            if not command:
                break
            conn.sendall(command.encode('utf-8'))
            response = conn.recv(1024)
            print(f"Response from {addr}: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Connection with {addr} ended: {e}")
    finally:
        conn.close()

# Function to start the server
def start_server(host, port, command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = server.accept()
            # Start a new thread for each client connection
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, command))
            client_thread.start()

if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all interfaces
    port = 9999       # Port to listen on
    start_server(host, port)
