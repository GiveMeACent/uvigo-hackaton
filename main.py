from utils import *

def main() :
  while True:
    devices = detectDevices()
    print(checkCamera(devices))
  
main()