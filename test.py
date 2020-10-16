from subprocess import Popen, PIPE
from rplidar import RPLidar
from data import Data
import re
import csv
import matplotlib.pyplot as plt
import time 
import math
from track import Track
from cluster import Cluster 
import keyboard
import sys

def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line

plt.style.use('ggplot')
fig = plt.figure(figsize=(13,6))
ax = fig.add_subplot(111)

def live_plotter(X,Y,line1,identifier='',pause_time=0.05):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        # create a variable for the line so we can later update it
        # line1, = ax.plot(X,Y)        
        #update plot label/title
        # plt.scatter(X,Y)
        ax.grid(True)
        for i in range(len(X)-1):
            if i == 0:
                ax.arrow(X[0],Y[0],X[1]-X[0],Y[1]-Y[0],head_width=0.2, head_length=0.2, fc='red', ec='black')
                # print("START POINT --> ("+str(X[0])+", "+str(Y[0])+")")
            elif i == len(X) - 2:
                ax.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],head_width=0.2, head_length=0.2, fc='black', ec='black')
                # print("END POINT   --> ("+str(X[i])+", "+str(Y[i])+")")
            else:
                ax.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],head_width=0.1, head_length=0.1, fc='lightblue', ec='lightblue')
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')          
        plt.xlim(-9.5,9.5)
        plt.ylim(-9.5,9.5)  
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
    
    # after the figure, axis, and line are created, we only need to update the y-data
    # line1.set_data(x_vec,y1_data)
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

def convert(point):
    rad = math.radians(point[0])
    return [abs(point[1])*math.cos(rad),abs(point[1])*math.sin(rad)]

# def cart2pol(x, y):
#     rho = np.sqrt(x**2 + y**2)
#     phi = np.arctan2(y, x)
#     return(rho, phi)

def cart_to_polar(point):
    # print("POINT:"+str(point))
    radius = math.sqrt( math.pow(point[0],2) + math.pow(point[1],2))
    radian = math.atan2(point[1],point[0])
    if radian < 0:
        angle = 360 + math.degrees(radian)
    else:
        angle = math.degrees(radian)
    return [angle,radius]

tracks = []  # tracked points of an object in cart coordinates
track = []
if __name__ == "__main__":
    frames = []
    frame = []
    line1 = []
    lidar_data = []
    # time.sleep(5)
    try:
        for j,path in enumerate(run("./ultra_simple /dev/ttyUSB0")):
            if keyboard.is_pressed('q'):
                
                lidar = RPLidar("/dev/ttyUSB0")
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                sys.exit()
                break                 
            if j > 5:
                text = str(path)
                # print(text)
                text = re.sub(r"b'","",text)
                text = re.sub(r"S","",text)
                text = re.sub(r"theta: ","",text)
                text = re.sub(r"Dist: ",",",text)
                text = re.sub(r"Q: ",",",text)            

                with open('mod_data.csv', 'w') as f:
                    for item in text:
                        f.write("%s" % item)
                
                
                # read modified data to a list
                with open("mod_data.csv",'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if float(row[1])/1000 != 0:
                            frame.append([float(row[0]),float(row[1])/1000])                        

                if len(frame) > 1:
                    if frame[-2][0] > frame[-1][0]:
                        # print("FRAME")
                        # print(frame)
                        
                        # lidar_data = []
                        # if track:
                        #     track_polar = cart_to_polar(tracks[-1])
                        #     for p in frame:
                        #         if p[0] < track_polar[0] + 20 and p[0] > track_polar[0] - 20:
                        #             lidar_data.append(p)
                        # else:    
                        #     lidar_data = frame
                        frames.append(frame)



                        # clustering 
                        cl = Cluster(frame)
                        # threshold = 0.3
                        clusters = cl.clusterByDistance() # polar coordinates  

                        #tracking
                        tr = Track(clusters) 
                        threshold_tr = 0.4
                        track = tr.track(tracks, threshold_tr) # caartesian coordinates
                        if track:
                            # print("NEAREST OBJECT POLAR:"+str(track_polar))
                            tracks.append(track)

                            X_VAL, Y_VAL = [],[]
                            # print("TRACK:")
                            # print(track)
                            try:
                                for p in tracks: 
                                    # cart = cart_to_polar(p)
                                    X_VAL.append(p[0])
                                    Y_VAL.append(p[1])
                                line1 = live_plotter(X_VAL,Y_VAL,line1)
                            except IndexError:
                                print("p:"+str(p))
                                print("NO TRACK DETECTED")
                        frame = []

        plt.show()



    except KeyboardInterrupt:
        lidar = RPLidar("/dev/ttyUSB0")
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        # print("The program stopped...")