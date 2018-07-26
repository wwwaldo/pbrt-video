% make bucky ball
gr = (1+sqrt(5))/2;
ico = allsigns(allcircs([1 0 gr]/2));
nv = size(ico,1);
d = zeros(nv);
for i=1:nv; 
  for j=1:nv
    e = ico(i,:)-ico(j,:);
    len = e*e';
    if len > .1 && len < 1.1
      d(i,j) = len;
    end
  end
end

b = [];

for i = 1:nv; 
  for j = 1:nv;
    if d(i,j) ~=0
      b(end+1,:) = (2*ico(i,:)+ico(j,:))/3;
      b(end+1,:) = (ico(i,:)+2*ico(j,:))/3;
    end
  end
end
e=b(1,:)-b(2,:);
scale = sqrt(e*e');

b = b/scale;
