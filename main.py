from time import sleep
from utils import *


def main():
    while True:
        devices = detectDevices()
        cameraId = checkCamera(devices)
        if (cameraId != ""):
            log("Camera recognized correctly.")
            sleep(3)
            break

    with open("config.json") as f:
        d = json.load(f)
        id = d["supported_cameras"][0]["id"]
        folder = d["supported_cameras"][0]["folder"]

    createFileStruct(id)
    downloadFiles(f"/media/{getUsername()}/{folder}/DCIM",
                  os.path.expanduser("~/media") + f"/{id}")

    videos = getVideosList(os.path.expanduser("~/media") + f"/{id}")
    for video in videos:
        stabilizeVideo(os.path.expanduser("~/media") + f"/{id}", video)


main()
