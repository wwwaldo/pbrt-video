#!/usr/bin/python3
# (works with python2 or python3)

#
# schlafli_interpreter.py
# Author: Don Hatch
# For: https://codegolf.stackexchange.com/questions/114280/schl%C3%A4fli-convex-regular-polytope-interpreter
#
# Print the vertex coords and per-element (edges, faces, etc.) vertex index
# lists of a regular polytope, given by its schlafli symbol {p,q,r,...}.
# The output polytope will have edge length 1 and will be in canonical position
# and orientation, in the following sense:
#  - the first vertex is the origin,
#  - the first edge lies along the +x axis,
#  - the first face is in the +y half-plane of the xy plane,
#  - the first 3-cell is in the +z half-space of the xyz space, etc.
# Other than that, the output lists are in no particular order.
#

import argparse
import sys
from math import *

# vector minus vector.
def vmv(a,b): return [x-y for x,y in zip(a,b)]
# matrix minus matrix.
def mmm(m0,m1): return [vmv(row0,row1) for row0,row1 in zip(m0,m1)]
# scalar times vector.
def sxv(s,v): return [s*x for x in v]
# scalar times matrix.
def sxm(s,m): return [sxv(s,row) for row in m]
# vector dot product.
def dot(a,b): return sum(x*y for x,y in zip(a,b))
# matrix outer product of two vectors; that is, if a,b are column vectors: a*b^T
def outer(a,b): return [sxv(x,b) for x in a]
# vector length squared.
def length2(v): return dot(v,v)
# distance between two vectors, squared.
def dist2(a,b): return length2(vmv(a,b))
# matrix times vector, homogeneous (i.e. input vector ends with an implicit 1).
def mxvhomo(m,v): return [dot(row,v+[1]) for row in m]
# Pad a square matrix (rotation/reflection) with an extra column of 0's on the
# right (translation).
def makehomo(m): return [row+[0] for row in m]
# Expand dimensionality of homogeneous transform matrix by 1.
def expandhomo(m): return ([row[:-1]+[0,row[-1]] for row in m]
                         + [[0]*len(m)+[1,0]])
# identity matrix
def identity(dim): return [[(1 if i==j else 0) for j in range(dim)]
                                               for i in range(dim)]
# https://en.wikipedia.org/wiki/Householder_transformation. v must be unit.
# Not homogeneous (makehomo the result if you want that).
def householderReflection(v):
  return mmm(identity(len(v)), sxm(2, outer(v,v)))

def sinAndCosHalfDihedralAngle(schlafli):
  # note, cos(pi/q)**2 generally has a nicer expression with no trig and often
  # no radicals, see http://www.maths.manchester.ac.uk/~cds/articles/trig.pdf
  ss = 0
  for q in schlafli:
    ss = cos(pi/q)**2 / (1 - ss)
  if abs(1-ss) < 1e-9:
    ss = 1  # prevent glitch in planar tiling cases
  return sqrt(ss), sqrt(1 - ss)


# Calculate a set of generators of the symmetry group of a {p,q,r,...} with
# edge length 1.
# Each generator is a dim x (dim+1) matrix where the square part is the initial
# orthogonal rotation/reflection and the final column is the final translation.
def calcSymmetryGenerators(schlafli):
  dim = len(schlafli) + 1
  if dim == 1: return [[[-1,1]]]  # one generator: reflect about x=.5
  facetGenerators = calcSymmetryGenerators(schlafli[:-1])
  # Start with facet generators, expanding each homogeneous matrix to full
  # dimensionality (i.e. from its previous size dim-1 x dim to dim x dim+1).
  generators = [expandhomo(gen) for gen in facetGenerators]
  # Final generator will reflect the first facet across the hyperplane
  # spanned by the first ridge and the entire polytope's center,
  # taking the first facet to a second facet also containing that ridge.
  # v = unit vector normal to that bisecting hyperplane
  #   = [0,...,0,-sin(dihedralAngle/2),cos(dihedralAngle/2)]
  s,c = sinAndCosHalfDihedralAngle(schlafli)
  v = [0]*(dim-2) + [-s,c]
  generators.append(makehomo(householderReflection(v)))
  return generators

#
# NOTE(andychu): Can we get rid of this ???  Seems ugly.
#

# Key for comparing coords with roundoff error.  Makes sure the formatted
# numbers are not very close to 0, to avoid them coming out as "-0" or "1e-16".
# This isn't reliable in general, but it suffices for this application
# (except for very large {p}, no doubt).

def vert2key(vert):
  return ' '.join(['%.9g' % (x+.123) for x in vert])


# Returns a pair verts,edgesEtc where edgesEtc is [edges,faces,...]
def regular_polytope(schlafli):
  dim = len(schlafli) + 1
  if dim == 1:
    return [[0],[1]], []  # base case

  gens = calcSymmetryGenerators(schlafli)

  facetVerts, facetEdgesEtc = regular_polytope(schlafli[:-1])

  # First get all the verts, and make a multiplication table.
  # Start with the verts of the first facet (padded to full dimensionality),
  # so indices will match up.
  verts = [facetVert+[0] for facetVert in facetVerts]
  vert2index = dict([[vert2key(vert), i] for i, vert in enumerate(verts)])
  multiplicationTable = []

  iVert = 0
  while iVert < len(verts):  # while verts is growing
    multiplicationTable.append([None] * len(gens))
    for iGen in range(len(gens)):
      newVert = mxvhomo(gens[iGen], verts[iVert])
      newVertKey = vert2key(newVert)
      if newVertKey not in vert2index:
        if len(verts) < vertexlimit:
          vert2index[newVertKey] = len(verts)
          verts.append(newVert)
        else:
          vert2index[newVertKey] = -1
      multiplicationTable[iVert][iGen] = vert2index[newVertKey]
    iVert += 1

  # The higher-level elements of each dimension are found by transforming
  # the facet's elements of that dimension.  Start by augmenting facetEdgesEtc
  # by adding one more list representing the entire facet.
  facetEdgesEtc.append([tuple(range(len(facetVerts)))])
  edgesEtc = []
  for facetElementsOfSomeDimension in facetEdgesEtc:
    elts = facetElementsOfSomeDimension[:]
    elt2index = dict([[elt, i] for i, elt in enumerate(elts)])
    iElt = 0
    while iElt < len(elts):  # while elts is growing
      for iGen in range(len(gens)):
        # andychu: Hm this is just generating a canonical sorted form for every
        # edge/face, and then we check it's already there?
        newElt = tuple(sorted([multiplicationTable[iVert][iGen]
                               for iVert in elts[iElt]]))
        if newElt[0] != -1:
          if newElt not in elt2index:  # deduplicate
            elt2index[newElt] = len(elts)
            elts.append(newElt)
      iElt += 1
    edgesEtc.append(elts)

  return verts, edgesEtc


# So input numbers can be like any of "8", "2.5", "7/3"
def parseNumberOrFraction(s):
  tokens = s.split('/')
  return float(tokens[0])/float(tokens[1]) if len(tokens)==2 else float(s)


vertexlimit = 1e100

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('numbers', type=str, nargs='+')
  parser.add_argument('-vlimit', type=int, default=-1)
  args = parser.parse_args()

  global vertexlimit
  #print(args.numbers)
  #print(args.vlimit)
  if args.vlimit != -1:  # TODO: Get rid of this?
    vertexlimit = args.vlimit

  schlafli = []
  for q in args.numbers:
    schlafli = schlafli + [parseNumberOrFraction(q)]

  verts, edgesEtc = regular_polytope(schlafli)

  # Hacky polishing of any integers or half-integers give or take rounding
  # error.
  def fudge(x):
    return round(2*x)/2 if abs(2*x-round(2*x))<1e-9 else x

  print(repr(len(verts))+' Vertices:')
  for v in verts:
    print(' '.join([repr(fudge(x)) for x in v]))

  for eltDim in range(1, len(edgesEtc)+1):
    print('')
    elts = edgesEtc[eltDim-1]
    if eltDim == 1:
      name1 = 'Edges' 
    elif eltDim == 2:
      name1 =  'Faces' 
    else:
      name1 = '%r-cells' % eltDim
    print('%d %s (%d vertices each)' % (len(elts), name1, len(elts[0])))
    for elt in elts:
      print(' '.join(str(i) for i in elt))

  # Assert the generalization of Euler's formula: N0-N1+N2-... = #
  # 1+(-1)**(dim-1).
  N = [len(elts) for elts in [verts]+edgesEtc]
  eulerCharacteristic = sum((-1)**i * N[i] for i in range(len(N)))
  print('')
  print('Euler characteristic: %s' % eulerCharacteristic)
  if 2.5 not in schlafli:
    assert eulerCharacteristic == 1 + (-1)**len(schlafli)

if __name__ == '__main__':
  main()
