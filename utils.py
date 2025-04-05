import json
from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID


def detectDevices() -> dict: 
  # Create the USBMonitor instance
  monitor = USBMonitor()

  # Get the current devices
  devicesDict = monitor.get_available_devices()

  # for device_id, device_info in devicesDict.items():
  #     print(f"DEVICE ID: {device_id} DEVICE MODEL: {device_info[ID_MODEL]} DEVICE ID MODEL ID: ({device_info[ID_MODEL_ID]} - DEVICE INFO: {device_info[ID_VENDOR_ID]})")
  
  return devicesDict

def checkCamera(devicesDict: dict) -> bool:
  found = False
  with open("config.json") as f:
    d = json.load(f)
    supported_camera = d["supported_cameras"][0]
    for device_id, device_info in devicesDict.items() :
      if (supported_camera["device_id"] == device_id and supported_camera["device_model"] == device_info[ID_MODEL] and supported_camera["device_model_id_model"] == device_info[ID_MODEL_ID] and supported_camera["device_info"] == device_info[ID_VENDOR_ID]) :
        found = True
        print(f"[INFO] Supported camera connected: {model_id} ({vendor_id})")
        createFileStruct(model_id)
        break
  
  return found
