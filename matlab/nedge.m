%NEDGE counts the edges of a polytope
%   NEDGE(M) finds the closest vertices, then reports all pairs at
%   this distance.

function ect = nedge(p)
  ect = size(edges(p),1);
  