import os
from datetime import datetime

def create_file_structure(device_name: str):
    base_path = os.path.expanduser("~/media") # user's home directory and ~/media as the base path


    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    device_folder = os.path.join(base_path, f"{device_name}_{timestamp}")     # Create a unique folder name based on the device name and current timestamp

    os.makedirs(os.path.join(device_folder, "videos"), exist_ok=True)
    os.makedirs(os.path.join(device_folder, "gcsv"), exist_ok=True)     # Create 'videos' and 'gcsv' subfolders inside the device folder

    print(f"[INFO] Created folders for {device_name} at {device_folder}")
    return device_folder
