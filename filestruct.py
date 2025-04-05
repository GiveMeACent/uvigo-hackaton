import os
from datetime import datetime

def create_file_structure(device_name: str):
    base_path = os.path.expanduser("~/media") # home directory + ~/media = base path
    
    device_folder = os.path.join(base_path, f"{device_name}")     

    os.makedirs(os.path.join(device_folder, "videos"), exist_ok=True)
    os.makedirs(os.path.join(device_folder, "gcsv"), exist_ok=True)     # videos, gcsv subfolders

    print(f"[INFO] Created folders for {device_name} at {device_folder}")
    return device_folder
