#!/usr/bin/python3
import sys
from scipy.spatial import ConvexHull
import numpy as np 

# Helper function
# Get new indices for face vertices if the convex hull has only a subset of the original input points.
def vertex_indices_to_subset(hull):
    vertex_translation = { 
            hull.vertices[i] : i
            for i in range(len(hull.vertices)) 
            }
    simplex_array = np.array(
            [ 
                [vertex_translation[j] for j in hull.simplices[i]]
                for i in range(len(hull.simplices)) 
            ],
            dtype=np.int32)
    return simplex_array

# Generate a PLY file for the 3-D convex hull of the input points.
def generate_ply(out, points):
    hull = ConvexHull(points)
    num_vertices = len(hull.vertices) 
    num_faces = hull.nsimplex
    
    with open('ply-header.template') as file:
        header = file.read()
    macro_replacements = {
        'num_vertices' : num_vertices,
        'num_faces'    : num_faces
    }

    polygon_faces = hull.simplices # each face has a list of vertex indices
    if num_vertices != hull.npoints:
        polygon_faces = vertex_indices_to_subset(hull)

    # Strings for vertices, faces PLY-formatted
    vertex_data = '\n'.join( [ ' '.join( map( "{:.4f}".format, points[i]))
                    for i in hull.vertices  ] )
    face_data = '\n'.join( [ '3 ' + ' '.join( map(str, polygon_faces[i]))
                    for i in range(num_faces) ] )

    print(header % macro_replacements, file=out)
    print(vertex_data, file=out)
    print(face_data, file=out)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Please specify a filename!")
    fname = sys.argv[1]

    points = np.random.rand(100, 3)
    with open(fname, 'w') as out:
        generate_ply(out, points)

