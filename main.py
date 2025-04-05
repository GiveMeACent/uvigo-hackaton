from utils import *


def main():
    while True:
        devices = detectDevices()
        cameraId = print(checkCamera(devices))
        if (cameraId != ""):
            break

    createFileStruct(cameraId)
    downloadFiles("/media/flamingfury/9C33-6BBD/DCIM",
                  os.path.expanduser("~/media"))


main()
