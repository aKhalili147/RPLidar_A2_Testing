from pprint import pprint
import math

class Track:

    def __init__(self, clusters):
        self.clusters = clusters

    def get_frame(self):
        return self.clusters 

    def compute_mean(self, clusters):
        cluster_mean = [] # mean values of each cluster in cartesian coordinates
        for i,cl in enumerate(clusters):
            sum_x, sum_y = 0, 0
            for point in cl:
                sum_x+=point[0]      
                sum_y+=point[1]      
            mean_x=sum_x/len(cl)
            mean_y=sum_y/len(cl)
            cluster_mean.append([mean_x,mean_y])

        return cluster_mean

    # convert polar coordinates to cartesian
    def convert(self, clusters):
        frame_cart = [[] for i in range(len(clusters))]
        for i,cluster in enumerate(clusters):
            for point in cluster:
                rad = math.radians(point[0])
                frame_cart[i].append([abs(point[1])*math.cos(rad),-abs(point[1])*math.sin(rad)])

        return frame_cart
    

    def track(self, tracks, threshold):
        track = [] # collection of points of each object track
        obj_track = []

        frame1_cart = self.convert(self.clusters)
        frame1_m = self.compute_mean(frame1_cart)
        # print("MEAN-VALUES IN FRAME-"+str(0))

        # find the nearest object 
        if tracks:
            obj_track = tracks[-1] # took the last tracked point of an object

            # create an interval for the last tracked point
            obj_borXp = obj_track[0]+threshold # x + epsilon 
            obj_borXn = obj_track[0]-threshold # x - epsilon
            obj_borYp = obj_track[1]+threshold # y + epsilon
            obj_borYn = obj_track[1]-threshold # y - epsilon            

            # find nearest point to last tracked point 
            nt_obj_dist = math.sqrt( math.pow(obj_track[0],2) + math.pow(obj_track[1],2)) 
            if frame1_m:
                for fm in frame1_m:
                    if (fm[0] > obj_borXn and fm[0] < obj_borXp) and  (fm[1] > obj_borYn and fm[1] < obj_borYp):
                        if abs(math.sqrt( math.pow(obj_track[0],2) + math.pow(obj_track[1],2)) - math.sqrt( math.pow(fm[0],2) + math.pow(fm[1],2)) ) < nt_obj_dist:
                            nt_obj_dist = abs(math.sqrt( math.pow(obj_track[0],2) + math.pow(obj_track[1],2)) - math.sqrt( math.pow(fm[0],2) + math.pow(fm[1],2)) )
                            track = fm 
                            
        else: 
            obj_track = frame1_m[0]
            nt_obj_dist = math.sqrt( pow(obj_track[0], 2) + pow(obj_track[1],2) )
            if frame1_m:
                for fm in frame1_m:
                    if math.sqrt( pow(fm[0], 2) + pow(fm[1], 2) ) < nt_obj_dist:
                        # print("before: "+str(nt_obj_dist))
                        nt_obj_dist =math.sqrt( pow(fm[0], 2) + pow(fm[1], 2) )
                        # print("after:  "+str(nt_obj_dist))
                        track = fm
        # print("NEAREST OBJECT: "+str(obj_track))

        return track 