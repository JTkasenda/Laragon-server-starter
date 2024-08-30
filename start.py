import subprocess
import os

# Path to the Laragon executable
laragon_path = r"C:\laragon\laragon.exe"  # Replace with your actual Laragon path

def start_laragon():
    try:
        # Start Laragon
        subprocess.run([laragon_path], check=True)
        print("Laragon started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Laragon: {e}")
    except FileNotFoundError:
        print("Laragon executable not found. Please check the path.")


if __name__ == "__main__":
    start_laragon()
