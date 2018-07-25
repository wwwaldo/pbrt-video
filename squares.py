import matplotlib.pyplot as plt 
import numpy as np 

def solve(line, plane):
    # These can also be done with dot products.
    a = np.matmul(plane.normal, line.direction)
    b = plane.d - np.matmul(plane.normal, line.translation)

    return np.linalg.solve(a, b)

class Plane:
    # input as lists.
    def __init__(self, normal, d):
        self.normal = np.array([normal])
        self.d = d
        return

class Line:
    def __init__(self, direction, translation):
        self.direction = np.transpose(np.array([direction]))
        self.translation = np.transpose(np.array([translation]))
        return


if __name__ == "__main__":
    print("Hello world!")

    for d in np.linspace( -1, 1, 10):
        line = Line([1, 0, 0], [1, 2, 3])
        plane = Plane([1, 1, 1], d)
        result = solve(line, plane)
        print(result)