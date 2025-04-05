from utils import *


def main():
    devices = detectDevices()
    while True:
        devices = detectDevices()
        cameraId = print(checkCamera(devices))
        if (cameraId != ""):
            log("Camera recognized correctly.")
            break

    with open("config.json") as f:
        d = json.load(f)
        folder = d["supported_cameras"][0]["folder"]

    createFileStruct(cameraId)
    downloadFiles(f"/media/{getUsername()}/{folder}/DCIM",
                  os.path.expanduser("~/media"))


main()
