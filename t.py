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

def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line

plt.style.use('ggplot')
# fig = plt.figure()
# ax = plt.axes()
fig = plt.figure(figsize=(13,6))
ax = fig.add_subplot(111)

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        # create a variable for the line so we can later update it
        # line1, = ax.plot(x_vec,y1_data)        
        #update plot label/title
        ax.clear()
        plt.scatter(x_vec,y1_data)
        ax.grid(True)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')          
        plt.xlim(-8,8)
        plt.ylim(-8,8)  
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

tracks = []  # tracked points of an object in cart coordinates

if __name__ == "__main__":
    frames = []
    frame = []
    line1 = []
    try:
        for j,path in enumerate(run("./ultra_simple /dev/ttyUSB0")):
            if j > 5:
                text = str(path)
                # print(text)
                text = re.sub(r"b'","",text)
                text = re.sub(r"S","",text)
                text = re.sub(r"theta: ","",text)
                text = re.sub(r"Dist: ",",",text)
                text = re.sub(r"Q: ",",",text)            

                print(list(text))

        #         with open('mod_data.csv', 'w') as f:
        #             for item in text:
        #                 f.write("%s" % item)
                
                
        #         # read modified data to a list
        #         with open("mod_data.csv",'r') as f:
        #             reader = csv.reader(f)
        #             for row in reader:
        #                 if float(row[1])/1000 != 0 and float(row[1])/1000 < 3:
        #                     frame.append([float(row[0]),float(row[1])/1000])

        #         # frame.append([float(text[0]),float(text[1])/1000])
        #         if len(frame) > 1:
        #             if frame[-2][0] > frame[-1][0]:
        #                 # print("FRAME")
        #                 # print(frame)
        #                 frames.append(frame)
                     

        #                 X_VAL, Y_VAL = [],[]
        #                 # print("TRACK:")
        #                 # print(track)
        #                 for p in frame: 
        #                     cart = convert(p)
        #                     X_VAL.append(cart[0])
        #                     Y_VAL.append(cart[1])
        #                 line1 = live_plotter(X_VAL,Y_VAL,line1)
        #                 frame = []
        # plt.show()



    except KeyboardInterrupt:
        lidar = RPLidar("/dev/ttyUSB0")
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        # print("The program stopped...")