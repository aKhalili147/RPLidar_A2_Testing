import math 

x = -2
y = -2

radius = math.sqrt( math.pow(x,2) + math.pow(y,2))
rad = math.atan2(y,x)
# angle = math.degrees(rad)
if rad < 0:
    angle = 360 + math.degrees(rad)
else:
    angle = math.degrees(rad)
print(angle)