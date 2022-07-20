import numpy as np

def distance(point_1, point_2):
    
    x1 = point_1[0]
    y1 = point_2[1]
    
    x2 = point_2[0]
    y2 = point_2[1]
    
    dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    return dist

def average(distances):
    
    added = 0 
    num_vals = 0
    for val in distances: 
        added = added + val 
        num_vals = num_vals + 1 
    
    return float(added)/float(num_vals)
