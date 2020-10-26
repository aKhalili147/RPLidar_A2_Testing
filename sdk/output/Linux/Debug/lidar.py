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
win.resize(1000,1000)
win.setWindowTitle('2-D Lidar Object Tracking')
win.setBackground('w')
p1 = win.addPlot(title="Nearest object tracking")
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

def test():
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

                        #tracking
                        tr = Track(clusters) 
                        threshold_tr = 0.4
                        track = tr.track(TRACKS, threshold_tr) # caartesian coordinates
                        # print("TRACKING:      --- %s seconds ---" % (time.time() - start_time))

                        if track:
                            # print("NEAREST OBJECT POLAR:"+str(track_polar))
                            TRACKS.append(track)                            

                            try:
                                frame_cart = convert(frame)
                                X = [p[0] for p in frame_cart]
                                Y = [p[1] for p in frame_cart]
                                curve2.setData(X,Y)

                                # if len(TRACKS) > 30:
                                #     for i,tr in enumerate(TRACKS[:20]):
                                #         del TRACKS[i]
                                X_VAL = [p[0] for p in TRACKS] 
                                Y_VAL = [p[1] for p in TRACKS]
                                curve1.setData(X_VAL,Y_VAL)
                                app.processEvents()

                            except IndexError:
                                print("NO TRACK DETECTED AT FRAME --> "+str(len(frames)))
                        frame = []
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
        QtGui.QApplication.instance().exec_()
