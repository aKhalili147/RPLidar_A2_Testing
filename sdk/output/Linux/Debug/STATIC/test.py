import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pprint import pprint
from data import Data
from cluster import Cluster
from track import Track
import math
import numpy as np
import time
import serial


class Test:

    # print("hello world")

    # def animate(i):

    #     data = Data(sys.argv[1]) # read data from Lidar

    #     polar_coor = data.mod_data() # modify data to readable format (polar coordinates)        

    #     cl = Cluster(polar_coor)

    #     threshold = 0.2 # threshold value for distance between consecutive points
    #     frames = cl.allFrame(threshold) # collection of all frames 
        
    #     tr = Track(frames)
        
    #     # tr.printFrames()
        
    #     threshold_f = 0.17
        
    #     tracks = tr.track(threshold_f)

    #     X, Y = [], []
    #     for p in tracks:
    #         X.append(p[0])
    #         Y.append(p[1])

    #     print("\t\tX axes values")
    #     print(X)
    #     print("\t\tY axes values")
    #     print(Y)
    #     ax = plt.axes()
    #     # for i in range(len(X)-1):
    #     #     if i == 0:
    #     #         ax.arrow(X[0],Y[0],X[1]-X[0],Y[1]-Y[0],head_width=0.07, head_length=0.07, fc='red', ec='black')
    #     #         print("START POINT --> ("+str(X[0])+", "+str(Y[0])+")")
    #     #     elif i == len(X) - 2:
    #     #         ax.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],head_width=0.05, head_length=0.05, fc='black', ec='black')
    #     #         print("END POINT   --> ("+str(X[i])+", "+str(Y[i])+")")
    #     #     else:
    #     #         ax.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],head_width=0.05, head_length=0.05, fc='lightblue', ec='black')
    #     plt.plot(X,Y)
    #     ax.grid(True)
    #     ax.spines['left'].set_position('zero')
    #     ax.spines['right'].set_color('none')
    #     ax.spines['bottom'].set_position('zero')
    #     ax.spines['top'].set_color('none')          
    #     plt.xlim(-6,6)
    #     plt.ylim(-6,6)  
    #     time.sleep(.25)


    # ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    # # plt.tight_layout()
    # plt.show()

    # DATA
    data = Data(sys.argv[1]) # read data from Lidar
    polar_coor = data.mod_data() # modify data to readable format (polar coordinates)
    # print(polar_coor)

    
    # CLUSTERING 
    cl = Cluster(polar_coor)
    # polarNonZero, zero = cl.clear_zeros(polar_coor)
    # print("length of zero: "+str(len(zero)))
    # print("polarNonZero: "+str(polarNonZero))
    # print("length of polarNonZero: "+str(len(polarNonZero)))

    threshold = 0.2 # threshold value for distance between consecutive points
    # clusters = cl.clusterByDistance(threshold)
    frames = cl.allFrame(threshold) # collection of all frames 
    # pprint(frames[0])
    # print("NUMBER OF FRAMES: "+str(len(frames)))
    # pprint(frames)
    # clusters = cl.k_means(2)


    # EXAMPLE 
    colormap = ['r','g','b','y','c','m','gray','black','limegreen']
    counter=0

    # # PLOT CLASSIFICATION
    # for cluster in clusters:
    #     cluster_cart = cl.convert(cluster)
    #     if len(cluster_cart) > 5:
    #         # print("CLUSTER-"+str(counter+1)+": ")
    #         # print(cluster)
    #         X,Y = [],[]
    #         for point in cluster_cart:
    #             X.append(point[0])
    #             Y.append(point[1])
                
    #             # plt.scatter(X,Y,c=colormap[counter])

    #         ax = plt.gca()

    #         ax.plot(X, Y)
    #         ax.grid(True)
    #         ax.spines['left'].set_position('zero')
    #         ax.spines['right'].set_color('none')
    #         ax.spines['bottom'].set_position('zero')
    #         ax.spines['top'].set_color('none')

    #         plt.xlim(-6,6)
    #         plt.ylim(-6,6)
    #             # counter+=1


    # plt.title('classification')
    # # plt.xlabel('X axes')
    # # plt.ylabel('Y axes')
    # plt.show()


    # # PLOT CLASSIFICATION
    # for frame in frames:
    #     for cluster in frame:
    #         cluster_cart = cl.convert(cluster) 
    #         if len(cluster_cart) > 5:
    #             # print("CLUSTER-"+str(counter+1)+": ")
    #             # print(cluster)
    #             X,Y = [],[]
    #             for point in cluster_cart:
    #                 X.append(point[0])
    #                 Y.append(point[1])
                
    #             # plt.scatter(X,Y,c=colormap[counter])

    #             ax = plt.gca()

    #             ax.plot(X, Y)
    #             ax.grid(True)
    #             ax.spines['left'].set_position('zero')
    #             ax.spines['right'].set_color('none')
    #             ax.spines['bottom'].set_position('zero')
    #             ax.spines['top'].set_color('none')

    #             plt.xlim(-6,6)
    #             plt.ylim(-6,6)
    #             # counter+=1


    # plt.title('classification')
    # # plt.xlabel('X axes')
    # # plt.ylabel('Y axes')
    # plt.show()

    
    
    # TRACKING
    tr = Track(frames)
    # tr.printFrames()
    threshold_f = 0.17
    tracks = tr.track(threshold_f)
    print("\nLength of trajectory --> "+str(len(tracks)))
    # for i,cluster in enumerate(frames[45]):
    #     print("CLUSTER-"+str(i+1)+": ")
    #     print(cluster)    

    # clusters_kmeans = cl.k_means(k=5)


    # PLOT TRACKING
    # print("TRACKS")
    # pprint(tracks)

    # print("TRACK[0]->START POINT: ("+str(tracks[0][0])+", "+str(tracks[0][1])+")")

    X,Y = [],[]
    for p in tracks:
        X.append(p[0])
        Y.append(p[1])
                
    ax = plt.axes()
    for i in range(len(X)-1):
        if i == 0:
            ax.arrow(X[0],Y[0],X[1]-X[0],Y[1]-Y[0],head_width=0.07, head_length=0.07, fc='red', ec='black')
            print("START POINT --> ("+str(X[0])+", "+str(Y[0])+")")
        elif i == len(X) - 2:
            ax.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],head_width=0.05, head_length=0.05, fc='black', ec='black')
            print("END POINT   --> ("+str(X[i])+", "+str(Y[i])+")")
        else:
            ax.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],head_width=0.05, head_length=0.05, fc='lightblue', ec='black')
        # ax.quiver(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i],headwidth=0.01, headlength=0.01)
    # plt.grid()
            # plt.scatter(X,Y)
    # ax = plt.gca()
    # ax.plot(X, Y)
    ax.grid(True)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')          
    plt.xlim(-6,6)
    plt.ylim(-6,6)          
    # X, Y = [], []
    # plt.arrow(X[0],Y[0],X[1]-X[0],Y[1]-Y[0])
    plt.title("tracking")
    plt.show()









########################################################################

# read file to list
# with open("output.csv",'r') as f:
#     text = f.readlines()

# del text[:6] # remove first 6 lines from list (there are some letters)

# # clean data (remove "theta", "Dist", "Q")
# for i in range(len(text)):
#     text[i] = re.sub(r"S","",text[i])
#     text[i] = re.sub(r"theta: ","",text[i])
#     text[i] = re.sub(r"Dist: ",",",text[i])
#     text[i] = re.sub(r"Q: ",",",text[i])

# # write modified data to csv
# with open('mod_data.csv', 'w') as f:
#     for item in text:
#         f.write("%s" % item)

# with open("mod_data.csv",'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         polar_coor.append([float(row[0]),float(row[1])/1000])

# def clear_objects(data):
#     test = []
#     for i,p in enumerate(data):
#         if p[1] <= 2:
#             test.append(p)
#     return test

# polar_coor = clear_objects(polar_coor)

# def clear_zeros(data):
#     zero = []
#     for i,p in enumerate(data):
#         if p[1] == 0:
#             zero.append(p)
#             data.pop(i)
#     return data,zero


# # convert polar coordinates to cartesian
# def convert(data):
#     cart_coor = []
#     for item in data:
#         rad = math.radians(item[0])
#         cart_coor.append([float(item[1]*math.cos(rad)),float(item[1]*math.sin(rad))])
#     return cart_coor

# def clusterByDistance(data_polar, threshold):
#     caar_coor = convert(data_polar)
#     clusters = [] # store the list of clusters from dataset
#     centroid = [] # store the centroids 
#     diff_p = []

#     for i in range(len(data_polar)-1):
#         # print("i: "+str(i))
#         diff_p = abs(data_polar[i+1][1]-data_polar[i][1])
#         centroid.append(data_polar[i])

#         if diff_p > threshold:
#                 # print("data_polar["+str(i+1)+"]:"+str(data_polar[i+1]) )
#                 # print("data_polar["+str(i)+"]:"+str(data_polar[i]) )
#                 # print("data_polar["+str(i+1)+"] - "+"data_polar["+str(i)+"] = "+str(abs(data_polar[i+1][1]-data_polar[i][1])))
#             clusters.append(centroid)
#             centroid = []
#     clusters.append(centroid)

#     return clusters


# clusters.append(zero)

# sum_clusters = 0
# for cluster in clusters:
#     sum_clusters+=len(cluster)
# print("Total number of points in clusters: "+str(sum_clusters))

# pprint("# of clusters: "+str(len(clusters)))
# # for i,cluster in enumerate(clusters):
# #     print("CLUSTER-"+str(i+1)+": ")
# #     print(cluster)


# def compare_centers(centers1, centers2):
#     if len(centers1) != len(centers2):
#         print("error in size!")
#     else:
#         for i in range(len(centers1)):
#             for j in range(len(centers1[i])):
#                 if centers1[i][j] != centers2[i][j]:
#                     return True

#     return False

# def copy_array(centers1,centers2):
#     if len(centers1) != len(centers2):
#         print("error in size!")
#     else:
#         for i in range(len(centers1)):
#             centers1[i] = centers2[i]
        
# def k_means(arr_in,k):
#     # pick k random centers initially
#     ctrs = random.sample(arr_in,k)
#     # print("centers at the beginning: "+str(ctrs))
    
#     ctrs2 = random.sample(arr_in,k)

#     while True:

#         lt_cls = [[] for x in range(k)] # list of clusters

#         # filling clusters with points
#         for x in arr_in:
#             index = min_dist(x,ctrs)
#             lt_cls[index].append(x)

#         # calculate new centers
#         for i in range(len(lt_cls)):
#             sum_x, sum_y = 0.,0.
#             for point in lt_cls[i]:
#                 sum_x+=point[0]
#                 sum_y+=point[1]
#             if len(lt_cls[i]) > 0:
#                 ctrs2[i][0], ctrs2[i][1] = sum_x/len(lt_cls[i]), sum_y/len(lt_cls[i])

#         # print("centers: "+str(ctrs2))
#         # print("clusters "+str(lt_cls))

#         # to check centers are stable or not
#         if compare_centers(ctrs,ctrs2) == False: 
#             print("centers of clusters: "+str(ctrs))
#             return lt_cls
#         else:
#             copy_array(ctrs,ctrs2)


# def min_dist(x,ctrs):
#     dist = math.sqrt(math.pow(ctrs[0][0]-x[0],2)+math.pow(ctrs[0][1]-x[1],2))
#     index = 0
#     for i in range(len(ctrs)):
#         if dist > math.sqrt(math.pow(ctrs[i][0]-x[0],2)+math.pow(ctrs[i][1]-x[1],2)):
#             dist = math.sqrt(math.pow(ctrs[i][0]-x[0],2)+math.pow(ctrs[i][1]-x[1],2))
#             index = i
    
#     return index

# for i,cluster in enumerate(clusters):
#     print("CLUSTER-"+str(i+1)+": ")
#     print(cluster)