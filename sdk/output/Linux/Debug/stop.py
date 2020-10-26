from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
