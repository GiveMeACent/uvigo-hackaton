# from usbmonitor import USBMonitor
# from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID
import json
import subprocess

def detectDevices() -> list:
    result = subprocess.run(['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        devices = result.stdout.splitlines()
        return devices
    else:
        return f"Errore lsusb: {result.stderr}"

def checkCamera(devices: list) -> bool:
  found = False
  with open("config.json") as f:
    d = json.load(f)
    supported_camera = d["supported_cameras"][0]
    for device in devices :
       id = device.split()[5]
       if (id == supported_camera["id"]):
          found = True
  
  return found
