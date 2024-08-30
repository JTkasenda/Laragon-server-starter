import os
import subprocess

laragon_path = r"C:\laragon\laragon.exe"

def close_laragon():
    try:
        # Use taskkill command to terminate Laragon
        subprocess.run(["taskkill", "/IM", "laragon.exe", "/F"], check=True)
        print("Laragon closed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to close Laragon: {e}")

if __name__ == "__main__":
    close_laragon()
