from utils import *


def main():
    while True:
        devices = detectDevices()
        cameraId = print(checkCamera(devices))
        if (cameraId != ""):
            break

    deviceName = getDeviceFromSysfs(cameraId)
    mountPoint = getMountPointForDevice(deviceName)


main()
