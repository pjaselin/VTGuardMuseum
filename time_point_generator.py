'''
Script to produce random sequences of coordinates and corresponding timestamps
'''
from random import randint
#(x1,y1),(x2,y2),...
coordinates = []
timestamps = []
current_timestamp = 0
for i in range(20):
    coordinates.append((randint(600, 1400), randint(550,900)))
    current_timestamp += randint(10,15)
    timestamps.append(current_timestamp)

print(coordinates)
print(timestamps)