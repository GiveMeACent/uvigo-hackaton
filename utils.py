# from usbmonitor import USBMonitor
# from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID
import json
import subprocess
import os
import shutil
import pwd


def log(message: str):
    f = open("./logs.txt", "a")
    f.write(message + "\n")
    f.close()


def detectDevices() -> list:
    """
    Detects the USB devices connected to the computer using the `lsusb` command.

    Runs the `lsusb` command (with subprocess); captures the output; 
    returns a list of connected devices (each representing a connected USB device) 

    If the lsusb fails, an error message is returned

    Returns:

    list: A list of strings representing the detected devices up to the max_devices limit

    str: An error message if the `lsusb` command fails or if no devices of specified type are found
    """

    result = subprocess.run(
        ['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        devices = result.stdout.splitlines()
        return devices
    else:
        return f"lsusb error: {result.stderr}"


def checkCamera(devices: list) -> str:
    """
    Checks for the camera ID in the list of connected devices:

    looks through the list of connected USB devices and checks if any of them 
    matches the supported camera ID defined in `config.json` 

    Parameters:
        devices (list): A list of strings representing connected USB devices.
                        Each string contains information about a device, such as its ID.

    Returns:
        str: The camera ID if a match is found, or an empty string if no match is found.
    """

    foundId = ""
    with open("config.json") as f:
        d = json.load(f)
        supported_camera = d["supported_cameras"][0]
        for device in devices:
            id = device.split()[5]
            if (id == supported_camera["id"]):
                foundId = id

    return foundId


def getDeviceFromSysfs(usb_device_id: str) -> str:
    """ 
    Searches for the device path in /sys/bus/usb/devices/ using the attribute USB device ID to locate the specified USB device
    and return the path to its associated block device.

    Parameters:
        usb_device_id (str): The USB device ID.

    Returns:
        str: The device path in Linux or an empty string if no matching device is found.
    """
    usb_path = "/sys/bus/usb/devices/"
    for root, dirs, files in os.walk(usb_path):
        for dir_name in dirs:
            if usb_device_id in dir_name:
                # Looking for video devices like /dev/video0
                device_path = os.path.join(root, dir_name, "block")
                for block_device in os.listdir(device_path):
                    device_name = block_device
                    return f"/dev/{device_name}"

    return ""


def getMountPointForDevice(device_name) -> str:
    """
    Retrieves the mount point of a specified device using the `lsblk` command in Linux; 
    executes the `lsblk` command to get the block devices and their mount points.
    It then searches the output to find the mount point corresponding to the specified device name.

    Parameters:
        device_name (str): The name of the device whose mount point is to be found

    Returns:
        str: The mount point of the device if found and mounted (e.g., '/mnt/device_name').
             If the device is not mounted, returns "Device not mounted".
             If the device is not found, returns "Device not found".
             If there's an error executing `lsblk`, returns the error message.
    """

    # Run lsblk to get the device mount point."
    result_lsblk = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result_lsblk.returncode == 0:
        lsblk_output = result_lsblk.stdout.splitlines()

        # Check the output of lsblk or any issues.
        print("Output of lsblk: ")
        for line in lsblk_output:
            print(line)

        # Iterate over the lines of the lsblk output (header)
        # Skip the first line of the output (header)
        for line in lsblk_output[1:]:
            columns = line.split()
            if len(columns) >= 2:  # Check that there are at least two columns.
                device = columns[0]
                mount_point = columns[1]

                # Check if the device name matches
                if device == device_name:
                    if mount_point:
                        return mount_point  # Return the mount point
                    else:
                        return "Device not mounted"  # If it is not mounted
        # If the device was not found in the output.
        return "Device not found"
    else:
        return f"Error executing lsblk: {result_lsblk.stderr}"


def getUsername():
    # Use 'os.getuid()' to get the user ID of the current user, and then pass it to 'pwd.getpwuid' to get the user information.
    # The '[0]' index extracts the username from the user information.
    return pwd.getpwuid(os.getuid())[0]


def createFileStruct(device_name: str):
    """
    Creates a file structure to organize downloaded files for a given device under the user's home directory, 
    with a base folder named after the device name. 
    Includes two subfolders: one for storing video files and another for storing 
    GCSV files.

    Parameters:
        device_name (str): The name of the device (used to create a base folder).

    Returns:
        str: The path to the root folder created for the device (+ "videos" and "gcsv" subfolders).
    """
    base_path = os.path.expanduser(
        "~/media")  # home directory + "~/media" = base path

    device_folder = os.path.join(base_path, f"{device_name}")

    os.makedirs(os.path.join(device_folder, "videos"), exist_ok=True)
    os.makedirs(os.path.join(device_folder, "gcsv"),
                exist_ok=True)     # videos, gcsv subfolders

    print(f"Created folders for {device_name} at {device_folder}")
    return device_folder


def downloadFiles(origin: str, destination: str):
    if (not origin.endswith("/")):
        origin += "/"
    if (not destination.endswith("/")):
        destination += "/"

    files = os.listdir(origin)

    for file in files:
        if (file.endswith(".MP4") or file.endswith(".gcsv")):
            if (file.endswith(".MP4")):
                folder = "videos/"
            if (file.endswith(".gcsv")):
                folder = "gcsv/"

            if (not os.path.exists(destination + folder + file)):
                shutil.copy(origin + file, destination + folder + file)
