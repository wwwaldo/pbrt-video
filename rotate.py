#!/usr/bin/python3
from math import sqrt, pi, sin, cos
import numpy as np
import matplotlib.pyplot as plt
    

def distance(p1, p2):
    return sqrt( pow(abs(p1[0] - p2[0]), 2) + 
          pow(abs(p1[1] - p2[1]), 2) + 
          pow(abs(p1[2] - p2[2]), 2) )

def circle(center, radius, npoints, max_angle=2*pi):
    points = np.linspace(0, max_angle, npoints)
    
    # rotate in xy plane
    vals = np.array([ [radius * cos(x), radius * sin(x), 0] for x in points])
    vals += center
    
    return vals

if __name__ == "__main__":
    points = circle([1,0,0], 3, 100, pi/6)
    # slice points
    flatpoints = points[:, :2]
    xlinspace = np.linspace(0, 2 * pi, 100)

    print(distance([0,0,0], [1,0,0]))

    plt.plot(flatpoints[:,0], flatpoints[:,1])
    plt.show()






