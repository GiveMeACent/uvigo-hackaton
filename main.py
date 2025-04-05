from utils import *


def main():
    while True:
        devices = detectDevices()
        cameraId = print(checkCamera(devices))
        if (cameraId != ""):
            break

    createFileStruct(cameraId)
    downloadFiles("/media/flamingfury/GPARTED-LIV/DCIM",
                  os.path.expanduser("~/media"))


main()
