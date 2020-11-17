# using PyQt --> visualization of software

from pyfirmata import Arduino
import serial
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from subprocess import Popen, PIPE
from rplidar import RPLidar
import re
from data import Data
import time 
import math
from track import Track
from cluster import Cluster 

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Test")
win.resize(500,500)
win.setWindowTitle('2-D Lidar Object Tracking')
win.setBackground('w')
p1 = win.addPlot(title="Nearest object")
p2 = win.addPlot(title="System")
p1.showGrid(x=True, y=True)
p2.showGrid(x=True, y=True)
curve1 = p1.plot(pen=None, symbol='o')
curve2 = p2.plot(pen=None,symbol='o')

p2.setXRange(-8,8, padding=0)
p2.setYRange(-8,8, padding=0)
p1.setXRange(-8,8, padding=0)
p1.setYRange(-8,8, padding=0)


def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line

def convert(frame):
    frame_cart = []
    for point in frame:
        rad = math.radians(point[0])
        frame_cart.append([abs(point[1])*math.cos(rad),-abs(point[1])*math.sin(rad)])
    return frame_cart

def cartPolar(point):
    angle = int(math.degrees(math.atan2(point[1],point[0])))
    if angle < 0:
        return 360+angle
    else: 
        return angle

def test():
    
    
    """ 
    --> if you have a servo motor and arduino (any type) 
        --> comment out below code 
        --> line: 64,65, 107
    """
    # board = Arduino("/dev/ttyACM0") # create an object of pyfirmata
    # servo = board.get_pin('d:3:s') # set pin 3 for servo motor
    start_time = time.time()
    TRACKS = []  # tracked points of an object in cart coordinates
    frames = [] # store all data for each frame
    frame = [] # store the data coming from one spin --> aprox. 360-500 points

    PATH = "mod_data.csv"
    data = Data(PATH)
    
    try:
        for j,path in enumerate(run("./ultra_simple /dev/ttyUSB0")):
            if j > 5:                
                text = str(path)
                point = data.run(text)
                if point[1] != 0:
                    frame.append(data.run(text))

                if len(frame) > 1:
                    if frame[-2][0] > frame[-1][0]:
                        frames.append(frame)
                    
                        # clustering 
                        cl = Cluster(frame)
                        # threshold = 0.3
                        clusters = cl.clusterByDistance() # polar coordinates  
                        # print("CLUSTERING:    --- %s seconds ---" % (time.time() - start_time))

                        if clusters:
                            #tracking
                            tr = Track(clusters) 
                            threshold_tr = 0.2
                            track = tr.track(TRACKS, threshold_tr) # caartesian coordinates
                            # print("TRACKING:      --- %s seconds ---" % (time.time() - start_time))

                            if track:
                                # print("NEAREST OBJECT POLAR:"+str(track_polar))
                                TRACKS.append(track)                            
                                angle = cartPolar(track)
                                # print("ANGLE: "+str(angle))
                                delta = time.time() - start_time
                                if angle < 180 and angle > 0:
                                    start_time = time.time()
                                    servo.write(angle)
                                
                                try:
                                    frame_cart = convert(frame)
                                    X = [p[0] for p in frame_cart]
                                    Y = [p[1] for p in frame_cart]
                                    curve2.setData(X,Y)

                                    if len(TRACKS) > 40:
                                        for i,tr in enumerate(TRACKS[:20]):
                                            del TRACKS[i]
                                    X_VAL = [p[0] for p in TRACKS] 
                                    Y_VAL = [p[1] for p in TRACKS]
                                    curve1.setData(X_VAL,Y_VAL)
                                    app.processEvents()

                                except IndexError:
                                    print("NO TRACK DETECTED AT FRAME --> "+str(len(frames)))
                            frame = []
                        else:
                            print("NO CLUSTER DETECTED AT FRAME --> "+str(len(frames)))

            else:
                text = str(path)
                text = re.sub(r"b'","",text)
                text = re.sub(r"'","",text)
                print(text)
    except KeyboardInterrupt:
        lidar = RPLidar("/dev/ttyUSB0")
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        sys.exit()


if __name__ == '__main__':
    import sys
    test()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        status = QtGui.QApplication.instance().exec_()
        sys.exit(status)