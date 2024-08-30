import subprocess
import psutil
import time
class Launcher:
    def __init__(self, process_path, process_name):
        self.process_path = process_path
        self.process_name = process_name

    def start_process(self):
        if(self.is_process_running()):
            self.is_process_running();
        else:
            try:
                # Start Laragon
                print(f"Runing {self.process_name}...")
                subprocess.Popen([self.process_path])
                while not self.is_process_running():
                    time.sleep(1)
                print(f"{self.process_name} started successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to start {self.process_name}: {e}")
            except FileNotFoundError:
                print(f"{self.process_name} executable not found. Please check the path.")

    def close_process(self):
        if(self.is_process_running()):
            try:
                # Use taskkill command to terminate Laragon
                subprocess.Popen(["taskkill", "/IM", self.process_name, "/F"])
                print(f"{self.process_name} closed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to close {self.process_name} : {e}")
        else:
            pass

    def is_process_running(self):
        # Iterate through all running processes
        for process in psutil.process_iter(['name']):
            # Check if the process name matches 'laragon.exe'
            if process.info['name'] == self.process_name:
                return True