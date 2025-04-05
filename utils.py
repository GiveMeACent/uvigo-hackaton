from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID


def detectDevices() -> list: 
  # Create the USBMonitor instance
  monitor = USBMonitor()

  # Get the current devices
  devicesDict = monitor.get_available_devices()

  # Print them
  # for device_id, device_info in devicesDict.items():
  #     print(f"DEVICE ID: {device_id}\n DEVICE MODEL: {device_info[ID_MODEL]}\n DEVICE ID MODEL ID: ({device_info[ID_MODEL_ID]}\n - DEVICE INFO: {device_info[ID_VENDOR_ID]})")
  
  return devicesDict.items()

def checkCamera(devicesDict: list) -> None:
  return None