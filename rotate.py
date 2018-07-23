from math import sqrt, pi, sin, cos
import numpy as np
import matplotlib.pyplot as plt
    

def distance(p1, p2):
    return sqrt( pow(abs(p1[0] - p2[0]), 2) + 
          pow(abs(p1[1] - p2[1]), 2) + 
          pow(abs(p1[2] - p2[2]), 2) )

def circle(center, radius, npoints):
    points = np.linspace(0, 2 * pi, npoints)
    
    # rotate in xy plane
    vals = np.array([ [radius * cos(x), radius * sin(x), 0] for x in points])
    vals += center
    vals = np.round(vals, 4) # round to 4 decimals 
    
    return vals

if __name__ == "__main__":
    import numpy as np

    points = circle([1,0,0], 3, 100)
    # slice points
    flatpoints = points[:, :2]
    xlinspace = np.linspace(0, 2 * pi, 100)

    print(distance([0,0,0], [1,0,0]))

    plt.plot(flatpoints[:,0], flatpoints[:,1])
    plt.show()






