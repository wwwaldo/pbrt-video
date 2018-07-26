%FACES find the faces defined by angles
%   FACES(A) finds the plane equations
%   Angles are triple of vertices.
%   The three points are used to compute the linear plane equation
%   Roundoff is removed by picking a representative value for each.
%   Multiple solutions are singled up by unique('rows')
%

function f = faces(a,v)
  TOL = 1.e-7;
  m = size(a,1);
  n = size(v,2);
  planes = [];
  for i=1:m                            % all angles
    planes(i,:) = v(a(i,:),:)\ones(n,1);
  end

  [ps, pi] = sort(planes(:));          % collect like items
  pd  = diff(ps) < TOL;                % find transitions
  tmp = ps(1);                         % head of "equal" list
  for i=1:numel(pd)                    % use std rep for each value
    if pd(i)
      planes(pi(i+1)) = tmp;           % use unique value
    else
      tmp = ps(i+1);                   % new head of "equal"
    end
  end
  size(planes)
  f = unique(planes,'rows');
