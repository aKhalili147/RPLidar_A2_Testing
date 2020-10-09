import subprocess
import rplidar

cmd = "./ultra_simple /dev/ttyUSB0"

try:
    import os

    batcmd = 'dir'
    result_code = os.system(cmd + ' > output.txt')
    if os.path.exists('output.txt'):
        fp = open('output.txt', "r")
        output = fp.read()
        fp.close()
        os.remove('output.txt')
        print(output)
except KeyboardInterrupt:
    lidar = RPLidar('/dev/ttyUSB0')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
