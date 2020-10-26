import re
import csv 
from pprint import pprint
import time

class Data:

    def __init__(self, path):       
        self.path = path

    # read data
    def read_data(self):
        # read modified data to a list
        with open(self.path,'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # if float(row[1])/1000 != 0:# and float(row[1])/1000 < 3:
                return [float(row[0]),float(row[1])/1000]

    def write_data(self, text):
        with open(self.path, 'w') as f:
            for item in text:
                f.write("%s" % item)        

    def modify(self, text):
        text = re.sub(r"b'","",text)
        text = re.sub(r"S","",text)
        text = re.sub(r"theta: ","",text)
        text = re.sub(r"Dist: ",",",text)
        text = re.sub(r"Q: ",",",text)
        return text 

    def clear_zeros(self, data):
        for i,point in enumerate(data):
            if point[1] == 0:
                del data[i]

        return data

    def run(self, text):
        text = self.modify(text)                    
        self.write_data(text) # read data from output.csv to text format
        data = self.read_data()
        return data