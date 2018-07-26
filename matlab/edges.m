%EDGES find the edges of a vertex set
%   EDGES(M) finds the closest vertices, then reports all pairs at
%   this distance.

function [s,f] = edges(p)
  m = size(p,1);
  d = inf(m);                          % distance matrix
  for i=1:m
    for j=i+1:m
      seg = p(i,:)-p(j,:);             % vertex pairs
      d(i,j) = sqrt(seg*seg');         % distance between
    end
  end
  
  es = min(d(:));                      % nearest neighbors
  TOL = es/10000;
  [s,f] = find(abs(d-es)<TOL);         % compensate for roundoff
