import socket 
import json
import launcher as  L
# Define server IP and port number
HOST = "127.0.0.1"
# Define server port number
PORT = 12345
# Path to Laragon.exe file. Replace with your actual Laragon installation path.
laragon_path = r"C:\laragon\laragon.exe"

laragon = L.Launcher(laragon_path, "laragon.exe")

try:
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to connect...")
    # Connect to the server using the IP address and port number
    client.connect((HOST,PORT))
    print("Connected successfully.")
    client.send(b"get_processes")
    print("Request sent.")
    buffer = b""
    while True:
        part = client.recv(1024)
        if not part:
            break
        buffer += part

    response = buffer.decode("utf-8")
    print("Response received.")
    processes = json.loads(response)

    for proc in processes:
        if "laragon.exe" not in proc:
            laragon.start_process()            
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    client.close()
