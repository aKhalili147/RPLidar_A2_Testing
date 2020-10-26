import math
import random
from pprint import pprint


class Cluster:

    def __init__(self, data):
        self.data = data


    def clearByDistance(self,polar_data):
        test = []
        for i,p in enumerate(polar_data):
            if p[1] <= 4:
                test.append(p)
        return test

    def clear_zeros(self,polar_data):
        zero = [] # origin points
        non_zero = []
        for p in polar_data:
            if p[1] == 0:
                zero.append(p)
            else:
                non_zero.append(p)
        return non_zero,zero

    # convert polar coordinates to cartesian
    def convert(self, polar_data):
        cart_coor = []
        for item in polar_data:
            rad = math.radians(item[0])
            cart_coor.append([abs(item[1])*math.cos(rad),abs(item[1])*math.sin(rad)])
        return cart_coor



    def clusterByDistance(self):
        threshold = 0.15
        clusters = [] # store the list of clusters from dataset
        centroid = [] # store the centroids 
        diff_p = 0
        
        for i in range(len(self.data)-1):
            diff_p = abs(self.data[i+1][1]-self.data[i][1]) # compute distance between two consecutive points
            diff_a = abs(self.data[i+1][0]-self.data[i][0]) # compute angle between two consecutive points
            centroid.append(self.data[i])

            if diff_p > threshold:
                clusters.append(centroid)
                centroid = []


        clusters = [cluster for cluster in clusters if cluster != [] and len(cluster) > 2]

        # pprint(clusters)
        return clusters


    # cluster by k-means
    def compare_centers(self,centers1, centers2):
        if len(centers1) != len(centers2):
            print("error in size!")
        else:
            for i in range(len(centers1)):
                for j in range(len(centers1[i])):
                    if centers1[i][j] != centers2[i][j]:
                        return True

        return False

    def copy_array(self,centers1,centers2):
        if len(centers1) != len(centers2):
            print("error in size!")
        else:
            for i in range(len(centers1)):
                centers1[i] = centers2[i]

    def min_dist(self,x,ctrs):
        dist = math.sqrt(math.pow(ctrs[0][0]-x[0],2)+math.pow(ctrs[0][1]-x[1],2))
        index = 0
        for i in range(len(ctrs)):
            if dist > math.sqrt(math.pow(ctrs[i][0]-x[0],2)+math.pow(ctrs[i][1]-x[1],2)):
                dist = math.sqrt(math.pow(ctrs[i][0]-x[0],2)+math.pow(ctrs[i][1]-x[1],2))
                index = i
        
        return index

    # def clearByCoordinates(self, cart_crd):
    #     test = []
    #     for i,p in enumerate(cart_crd):
    #         if math.sqrt(math.pow(p[0],2)+math.pow(p[1],2)) <= 1.5:
    #             test.append(p)
    #     return test

    def k_means(self,k):
        one_frame = self.one_frame()
        cart = self.convert(one_frame)
        cartNonZero, zero = self.clear_zeros(cart) # get rid of objects, distance=0 
        cartNonZero = self.clearByCoordinates(cartNonZero)
        # cartNonZero = self.convert(polarNonZero)

        # pick k random centers initially
        ctrs = random.sample(cartNonZero,k)
        print("centers at the beginning: "+str(ctrs))       
        ctrs2 = random.sample(cartNonZero,k)

        while True:

            lt_cls = [[] for x in range(k)] # list of clusters

            # filling clusters with points
            for x in cartNonZero:
                index = self.min_dist(x,ctrs)
                lt_cls[index].append(x)

            # calculate new centers
            for i in range(len(lt_cls)):
                sum_x, sum_y = 0.,0.
                for point in lt_cls[i]:
                    sum_x+=point[0]
                    sum_y+=point[1]
                if len(lt_cls[i]) > 0:
                    ctrs2[i][0], ctrs2[i][1] = sum_x/len(lt_cls[i]), sum_y/len(lt_cls[i])

            print("centers: "+str(ctrs2))
            # print("clusters "+str(lt_cls))

            # to check centers are stable or not
            if self.compare_centers(ctrs,ctrs2) == False: 
                lt_cls.append(zero)
                # print("centers of clusters: "+str(ctrs))
                return lt_cls
            else:
                self.copy_array(ctrs,ctrs2)

