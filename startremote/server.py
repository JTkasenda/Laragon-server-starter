import socket
import threading

# Function to handle Apache process execution
def handle_apache(conn, addr, apache_command):
    try:
        print(f"Starting Apache on {addr}")
        conn.sendall(apache_command.encode('utf-8'))
        response = conn.recv(1024)
        print(f"Apache response from {addr}: {response.decode('utf-8')}")
    except socket.error as se:
        print(f"Socket error with Apache on {addr}: {se}")
    except Exception as e:
        print(f"Unexpected error with Apache on {addr}: {e}")
    finally:
        try:
            conn.close()
        except socket.error as se:
            print(f"Error closing connection for Apache on {addr}: {se}")

# Function to handle MySQL process execution
def handle_mysql(conn, addr, mysql_command):
    try:
        print(f"Starting MySQL on {addr}")
        conn.sendall(mysql_command.encode('utf-8'))
        response = conn.recv(1024)
        print(f"MySQL response from {addr}: {response.decode('utf-8')}")
    except socket.error as se:
        print(f"Socket error with MySQL on {addr}: {se}")
    except Exception as e:
        print(f"Unexpected error with MySQL on {addr}: {e}")
    finally:
        try:
            conn.close()
        except socket.error as se:
            print(f"Error closing connection for MySQL on {addr}: {se}")

# Function to start the server
def start_server(host, port, apache_path, mysql_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((host, port))
            server.listen()
            print(f"Server listening on {host}:{port}")
            while True:
                try:
                    conn, addr = server.accept()
                    print(f"New connection from {addr}")

                    # Start a new thread for each process
                    apache_thread = threading.Thread(target=handle_apache, args=(conn, addr, apache_path))
                    mysql_thread = threading.Thread(target=handle_mysql, args=(conn, addr, mysql_path))         
                    
                    apache_thread.start()
                    mysql_thread.start()

                except socket.error as se:
                    print(f"Socket error while accepting connections: {se}")
                except Exception as e:
                    print(f"Unexpected error while accepting connections: {e}")
    except socket.error as se:
        print(f"Server socket error: {se}")
    except Exception as e:
        print(f"Unexpected server error: {e}")

if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all interfaces
    apache_path = r"C:\laragon\bin\apache\Apache24\bin\httpd.exe"
    mysql_path = r"C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysqld.exe"
    port = 9999       # Port to listen on
    start_server(host, port, apache_path, mysql_path)
