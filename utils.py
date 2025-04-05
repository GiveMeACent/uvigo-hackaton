# from usbmonitor import USBMonitor
# from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID
import json
import subprocess
import os


def detectDevices() -> list:
    result = subprocess.run(
        ['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        devices = result.stdout.splitlines()
        return devices
    else:
        return f"lsusb error: {result.stderr}"


def checkCamera(devices: list) -> str:
    foundId = ""
    with open("config.json") as f:
        d = json.load(f)
        supported_camera = d["supported_cameras"][0]
        for device in devices:
            id = device.split()[5]
            if (id == supported_camera["id"]):
                foundId = id

    return foundId


def getDeviceFromSysfs(usb_device_id) -> str:
    usb_path = "/sys/bus/usb/devices/"

    for root, dirs, files in os.walk(usb_path):
        for dir_name in dirs:
            if usb_device_id in dir_name:
                # Trova il dispositivo /dev associato
                device_path = os.path.join(root, dir_name, "block")
                for block_device in os.listdir(device_path):
                    device_name = block_device
                    return f"/dev/{device_name}"

    return ""

def getMountPointForDevice(device_name) -> str:
    # Esegui lsblk per ottenere il punto di montaggio del dispositivo
    result_lsblk = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result_lsblk.returncode == 0:
        lsblk_output = result_lsblk.stdout.splitlines()

        # Controlliamo l'output di lsblk per eventuali problemi
        print("Output di lsblk:")
        for line in lsblk_output:
            print(line)

        # Iteriamo sulle righe dell'output di lsblk
        # Salta la prima riga dell'output (intestazione)
        for line in lsblk_output[1:]:
            columns = line.split()
            if len(columns) >= 2:  # Verifica che ci siano almeno due colonne
                device = columns[0]
                mount_point = columns[1]

                # Controlla se il nome del dispositivo corrisponde
                if device == device_name:
                    if mount_point:
                        return mount_point  # Restituisci il punto di montaggio
                    else:
                        return "Dispositivo non montato"  # Se non è montato
        # Se il dispositivo non è stato trovato nell'output
        return "Dispositivo non trovato"
    else:
        return f"Errore nell'eseguire lsblk: {result_lsblk.stderr}"

def createFileStruct(device_name: str):
    base_path = os.path.expanduser("~/media") # home directory + "~/media" = base path
    
    device_folder = os.path.join(base_path, f"{device_name}")     

    os.makedirs(os.path.join(device_folder, "videos"), exist_ok=True)
    os.makedirs(os.path.join(device_folder, "gcsv"), exist_ok=True)     # videos, gcsv subfolders

    print(f"Created folders for {device_name} at {device_folder}")
    return device_folder
