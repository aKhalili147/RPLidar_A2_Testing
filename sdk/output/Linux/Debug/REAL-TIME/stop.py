from rplidar import RPLidar
import sys

lidar = RPLidar('/dev/ttyUSB0')
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
sys.exit()
