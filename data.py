import re
import csv 
from pprint import pprint
import time

class Data:

    def __init__(self, path):       
        self.path = path

    # read data
    def read_data(self):
        with open(self.path,'r') as f:
            text = f.readlines()
        return text


    # clean data
    def mod_data(self):

        text = self.read_data() # read data from output.csv to text format
        
        data = [] # to store angle, distance attributes
        
        del text[:6] # remove first 6 lines from list (there are some letters)
        
        # clean data (remove "theta", "Dist", "Q") using regex
        for i in range(len(text)):
            text[i] = re.sub(r"b'","",text[i])
            text[i] = re.sub(r"S","",text[i])
            text[i] = re.sub(r"theta: ","",text[i])
            text[i] = re.sub(r"Dist: ",",",text[i])
            text[i] = re.sub(r"Q: ",",",text[i])
        
        # write modified data to csv
        with open('mod_data.csv', 'w') as f:
            for item in text:
                f.write("%s" % item)
        
        
        # read modified data to a list
        with open("mod_data.csv",'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append([float(row[0]),float(row[1])/1000])
        # pprint(data)
        return data
