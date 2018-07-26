function dist(ei, ej)
  n = max(max(ei), max(ej));
  d0 = (1:n)';
  d1 = [ei ej];
  d1 = [sort(d1,2); sort(d1,2,'descend')];
  d1 = unique(d1, 'rows');
  edges = size(d1)
  d2 = [];
  for i=1:size(d1,1)
    c = d1(i,2);
    for j=1:size(d1,1)
      if c == d1(j,1) && d1(j,2) ~= d1(i,1)
        d2(end+1,:) = [d1(i,:), d1(j,2)];
      end
    end
  end
  angles = size(d2)
  d3 = [];
  for i=1:size(d2,1)
    c = d2(i,3);
    for j=1:size(d1,1)
      if c == d1(j,1) && d1(j,2) ~= d2(i,2)
        d3(end+1,:) = [d2(i,:), d1(j,2)];
      end
    end
  end
  triples = size(d3)
  
