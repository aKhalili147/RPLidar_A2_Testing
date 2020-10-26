from pprint import pprint
import math

class Track:

    def __init__(self, clusters):
        self.clusters = clusters

    def get_frame(self):
        return self.clusters 

    def compute_mean(self, clusters):
        # pprint(frame)
        cluster_mean = []
        for cl in clusters:
            if cl:
                sum_angle = 0
                sum_dist = 0
                for p in cl:
                    sum_angle+=p[0]      
                    sum_dist+=p[1]      
                m_angel=sum_angle/len(cl)
                m_dist=sum_dist/len(cl)
                cluster_mean.append([m_angel,m_dist])

        return cluster_mean

    # convert polar coordinates to cartesian
    def convert(self, clusters):
        # pprint(clusters[1][1])
        # pprint(clusters)
        frame_m = []
        cart_coor = []
        for cluster in clusters:
            if cluster:
                for point in cluster:
                    # print(point[0])
                    rad = math.radians(point[0])
                    cart_coor.append([abs(point[1])*math.cos(rad),-abs(point[1])*math.sin(rad)])
                frame_m.append(cart_coor)
                cart_coor = []

        return frame_m


    def clearByDistance(self,polar_data):
        test = []
        for i,p in enumerate(polar_data):
            if p[1] <= 2:
                test.append(p)
        return test    

    def track(self, tracks, threshold):
        track = [] # collection of points of each object track
        obj_track = []

        frame1_cart = self.convert(self.clusters)
        frame1_m = self.compute_mean(frame1_cart)
        # print("MEAN-VALUES IN FRAME-"+str(0))
        # pprint(frame1_m)
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

        # for i in range(len(self.frames )-1):
            
        #     # print("nearest object --> "+str(obj_track))

        #     # if there is no object detected
        #     if not obj_track:
        #         print("***ANY OBJECT DETECTED***")
        #         continue
            

        #     # create an interval for the nearest object
        #     obj_borXp = obj_track[0]+threshold
        #     obj_borXn = obj_track[0]-threshold
        #     obj_borYp = obj_track[1]+threshold
        #     obj_borYn = obj_track[1]-threshold

        #     # print("obj_borXp:"+str(obj_borXp))
        #     # print("obj_borXn:"+str(obj_borXn))
        #     # print("obj_borYp:"+str(obj_borYp))
        #     # print("obj_borYn:"+str(obj_borYn))


        #     #next frame
        #     frame2_cart = self.convert(self.frames[i+1])
        #     frame2_m = self.compute_mean(frame2_cart)            
        #     # print("MEAN-VALUES IN FRAME-"+str(i+1))
        #     # pprint(frame2_m)

        #     obj_track2 = frame2_m[0]
        #     nt_obj_dist = math.sqrt( pow(obj_track2[0], 2) + pow(obj_track2[1],2) )
        #     for fm in frame2_m:
        #         if math.sqrt( pow(fm[0], 2) + pow(fm[1], 2) ) > nt_obj_dist:
        #             # print("before: "+str(nt_obj_dist))
        #             nt_obj_dist =math.sqrt( pow(fm[0], 2) + pow(fm[1], 2) )
        #             # print("after:  "+str(nt_obj_dist))
        #             obj_track2 = fm


        #     # add nearest point to the object in the next frame
        #     index = -1
        #     dist1 = math.sqrt( pow(obj_track[-1], 2) + pow(obj_track[-1],2) )
        #     dist2 = math.sqrt( pow(obj_track2[0], 2) + pow(obj_track2[1],2) )


        #     if dist1 <= dist2:
        #         for m2 in frame2_m:
        #             if (m2[0] < obj_borXp and m2[0] > obj_borXn) and (m2[1] < obj_borYp and m2[1] > obj_borYn):
        #                 obj_track = m2
        #         track.append(obj_track)
    
        #     # print("Tracjectory of tracked object:")
        #     # print(track)
            
        #     ## Method2
        #     # if track:
        #     #     min_dist = abs(math.sqrt( pow( track[0][-1][0],2) + pow( track[0][-1][1],2) ) - math.sqrt( pow(obj_track[0],2) + pow(obj_track[1],2) ) )
        #     #     rem = obj_track
        #     #     index = -1
        #     #     if len(track) > 1:
        #     #         for j, obj in enumerate(track[1:]):
        #     #             if math.sqrt( pow(obj[-1][0],2) + pow(obj[-1][1],2) - math.sqrt( pow(obj_track[0],2) + pow(obj_track[1],2) )) <  min_dist:
        #     #                 min_dist =math.sqrt( pow(obj[-1][0],2) + pow(obj[-1][1],2) - math.sqrt( pow(obj_track[0],2) + pow(obj_track[1],2) ))
        #     #                 # rem = obj
        #     #                 index = j
        #     #     if index == -1:
        #     #         track[0].append(obj_track)
        #     #     else:
        #     #         track[index].append(obj_track)
        #     # else:
        #     #     track.append([obj_track])


        # #     # # Mehtod1
        # #     # for i,m2 in enumerate(frame2_m):
        # #     #     min_dist = math.sqrt(math.pow(2,m2[0]) + math.pow(2,m2[1]) )
        # #     #     rem = m2
        # #     #     index = -1
        # #     #     obj_track = []
        # #     #     for j,obj in enumerate(track):
        # #     #         obj_dist = math.sqrt(math.pow(2,obj[-1][0])+math.pow(2,obj[-1][1]))                    
        # #     #         if abs(min_dist - obj_dist) < min_dist and (abs(m2[0] - obj[-1][0]) < threshold and abs(m2[1] - obj[-1][1]) < threshold):
        # #     #             min_dist = abs(min_dist-obj_dist)
        # #     #             rem = obj[-1]
        # #     #             index = j                    
        # #     #     # print("REMINDER: "+str(rem))
        # #     #     # print("Mean value: "+str(m2))

        # #     #     if abs(m2[1] - rem[1]) < threshold and abs(m2[0] - rem[0]) < threshold: 
        # #     #         # print("Added to:   "+str(rem))
        # #     #         # print("index: "+str(index))
        # #     #         obj_track.append([m2,index])
        # #     #     else:
        # #     #         # print("new object:"+str(rem))
        # #     #         obj_track.append([m2,-1])                                  

        # #     #     for obj in obj_track:
        # #     #         if obj[-1] == -1:
        # #     #             track.append([m2])
        # #     #         else:
        # #     #             track[obj[-1]].append(m2)

        
        # # for i,tr in enumerate(track):
        # #     if len(tr) < 5:
        # #         track[i].clear()
        
        
        # track = [tr for tr in track if tr != []]

        # # # print("TRACK")
        # # # pprint(track)

        # # # flag = True
        # # # obje = []
        # # # min_dist = math.sqrt( pow(2,track[0][-1][0]) + pow(2,track[0][-1][1]) )
        # # # for i,tr in enumerate(track):
        # # #     # print("CHECK")
        # # #     # pprint(track) 
        # # #     if math.sqrt( pow(2,tr[-1][0]) + pow(2,tr[-1][1]) ) < min_dist:
        # # #         pprint(tr)
        # # #         print("***")
        # # #         min_dist = math.sqrt( pow(2,tr[-1][0]) + pow(2,tr[-1][1]) )
        # # #         obje = tr
        # # #         flag = False

        # # # if flag == True:
        # # #     obje = track[0]       

        # # # print("OBJ TRACK")
        # # # print(obje)
        # return track


    def printFrames(self):
        for i,f in enumerate(self.frames):
            print("FRAME"+str(i)+":")
            print(f)

