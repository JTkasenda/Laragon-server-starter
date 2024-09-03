import socket
import threading
import subprocess
import time

# List of PCs with their IPs and service paths
pcs = [
    {'ip': '192.168.1.70', 'apache': r'C:\laragon\bin\apache\Apache24\bin\httpd.exe', 'mysql': r'C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysqld.exe'},
    {'ip': '192.168.1.65', 'apache': r'C:\laragon\bin\apache\Apache24\bin\httpd.exe', 'mysql': r'C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysqld.exe'},
    # Add more PCs as needed
]

down_pcs = set()

# Function to check if a PC is up and running
def is_pc_online(ip):
    try:
        with socket.create_connection((ip, 80), timeout=5):
            return True
    except Exception:
        return False

# Function to notify the user when a PC goes down
def notify_user(pc_ip):
    # This can be expanded to send an email, or trigger another form of alert
    print(f"ALERT: PC {pc_ip} is not responding!")

# Function to monitor PCs
def monitor_pcs():
    while True:
        for pc in pcs:
            ip = pc['ip']
            if not is_pc_online(ip):
                if ip not in down_pcs:
                    down_pcs.add(ip)
                    notify_user(ip)  # Notify only when the PC goes down
            else:
                if ip in down_pcs:
                    down_pcs.remove(ip)  # Remove from down list when it comes back online
        time.sleep(10)  # Adjust the interval as needed

# Function to manage Apache and MySQL services on the PC
def ensure_services_running(ip, apache_path, mysql_path):
    try:
        # Start Apache if not running
        subprocess.run(f'powershell -Command "Get-Process | Where-Object {{$_.Path -eq \'{apache_path}\'}}"', shell=True, check=True)
        subprocess.Popen(apache_path, creationflags=subprocess.CREATE_NEW_CONSOLE)

        # Start MySQL if not running
        subprocess.run(f'powershell -Command "Get-Process | Where-Object {{$_.Path -eq \'{mysql_path}\'}}"', shell=True, check=True)
        subprocess.Popen(mysql_path, creationflags=subprocess.CREATE_NEW_CONSOLE)

        print(f"Services on {ip} are running.")
    except Exception as e:
        print(f"Failed to start services on {ip}: {e}")

# Function to handle proxying the request
def proxy_request(conn, addr):
    while True:
        request = conn.recv(4096)
        if not request:
            break

        # Forward the request to the first available PC
        for pc in pcs:
            if is_pc_online(pc['ip']):
                ensure_services_running(pc['ip'], pc['apache'], pc['mysql'])

                try:
                    with socket.create_connection((pc['ip'], 80)) as backend_conn:
                        backend_conn.sendall(request)
                        while True:
                            response = backend_conn.recv(4096)
                            if not response:
                                break
                            conn.sendall(response)
                except Exception as e:
                    print(f"Failed to proxy to {pc['ip']}: {e}")
                break
        else:
            conn.sendall(b"HTTP/1.1 503 Service Unavailable\r\n\r\n")
            break

    conn.close()

# Function to start the proxy server
def start_proxy_server(host, port):
    # Start the PC monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_pcs)
    monitor_thread.daemon = True  # Daemonize thread so it stops when the main thread exits
    monitor_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"Proxy server listening on {host}:{port}")
        while True:
            conn, addr = server.accept()
            proxy_thread = threading.Thread(target=proxy_request, args=(conn, addr))
            proxy_thread.start()

if __name__ == "__main__":
    start_proxy_server("0.0.0.0", 9999)
