%NDROTATE rotate cartesian coordinates in N-D space
%   NDROTATE(M) builds a rotation matrix from a matrix of angles.
%   M(i,j) is the i-to-j rotation angle (radians)
%   M(i,i) is ignored.
%   Examples: 
%   ndrotate([0, pi/6]) is
%      0.8660   -0.5000
%      0.5000    0.8660
%   ndrotate([0, pi/6; pi/4, 0]) is
%      0.9659    0.2588
%     -0.2588    0.9659
%    Use:
%   cube = allsigns([1 1 1]/2);
%   rotatedcube = cube*ndrotate([0, 1, 2; .5 0 .3]);
%

function res = ndrotate(angles)
  [m,n] = size(angles);
  res = eye(n);
  for i=1:m
    for j=1:n
      if i ~= j && angles(i,j) ~= 0
        tmp = eye(n);
        tmp(i,i) = cos(angles(i,j));
        tmp(j,j) = tmp(i,i);
        tmp(i,j) = -sin(angles(i,j));
        tmp(j,i) = -tmp(i,j);
        res = res*tmp;
      end
    end
  end
  