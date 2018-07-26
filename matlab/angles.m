%ANGLES find the angles of an edge set
%   ANGLES(E) finds vertex triples
%

function a = angles(e)
  m = size(e,1);
  a = [];
  for i=1:m
    for j=i+1:m
      t = unique([e(i,:), e(j,:)]);
      if numel(t)==3; a(end+1,:) = t; end 
    end
  end
 