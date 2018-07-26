%NFACE counts the faces of a polyhedron
%   NFACE(M) uses Euler's formula V-E+F=2
%

function fct = nface(p)
  vct = size(p,1);
  ect = nedge(p);
  fct = ect-vct+2;