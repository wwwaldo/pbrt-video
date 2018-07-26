% FILE:     polyhedron.m
% PURPOSE:  general object representation of regular polytope

function poly = polyhedron(name);

TOL = 1.0E-6;
v = vertices(name);
dim = size(v, 2);
nv = size(v, 1);                       % vertex count

% edge-square matrix
d = zeros(nv);
for i=1:nv
  for j=i+1:nv
    ev = v(i,:)-v(j,:);
    d(i,j) = sum(ev.*ev);              % edge^2
  end
end

e2   = d(d(:)~=0);                     % nonzero edge^2 s
me   = min(e2);                        % smallest
edge = sqrt(me);                       % edge length
v    = v./edge;                        % scale to unit edge

% find edges
[i,j] = find(abs(me - d) < TOL);
e = reshape([i, j], numel(i), 2);      % edges
ne = size(e,1);                        % edge count

% vertex connectivity
c = inf(nv);
for i=1:nv
  c(i,i)=0;                            % distance 0
end

for i=1:ne
  j = e(i,1); k = e(i,2);
  c(j,k) = 1; c(k,j) = 1;              % distance 0&1
end

angles = [];
for i=1:nv
  nbr = [];
  for j=1:nv
    if c(i,j) == 1
      nbr(end+1) = j;                  % neighbors
    end
  end
  lim=numel(nbr);                      % how many neighbors
  for j=1:lim                          % all pairs of ne...
    for k=j+1:lim
      angles(end+1,:) = sort([i, nbr(j), nbr(k)]);
    end
  end
end
angles = unique(angles, 'rows');
size(angles,1)

planes = [];
for i=1:size(angles,1)                 % all angles
  planes(i,:) = v(angles(i,:),:)\ones(dim,1);
end

[ps, pi] = sort(planes(:));            % collect like items
pd  = diff(ps) < TOL;                  % find transitions
tmp = ps(1);                           % head of "equal" list
for i=1:numel(pd)                      % use std rep for each value
  if pd(i)
    planes(pi(i+1)) = tmp;             % use unique value
  else
    tmp = ps(i+1);                     % new head of "equal"
  end
end
planes = unique(planes, 'rows');       % single up the vectors
poly.vertices = v;
poly.edges = edges;
poly.planes = planes
