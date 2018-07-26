%BUCKYTUMBLE shows tumbling Bucky Ball
%   BUCKYTUMBLE -- display the Bucky Ball, slowly tumbling in space
%
%   Bill McKeeman

function buckytumble
  gr = (1+sqrt(5))/2;                  % golden ration
  d = @(a,b) a + b*gr;                 % vertex function
  bg = .8*[1 1 1];                     % background grey
  set(gcf, 'color', bg);

  bb = perms(...                       % Bucky Ball vertices
    [d(0,0), d(0,3), d(1,0)
     d(1,0), d(0,2), d(2,1)
     d(2,0), d(0,1), d(1,2)]/2, 'cycles', 'signs', 'unique');

  mx = max(abs(bb(:)))*1.2;            % frame the picture
  axis([-mx mx -mx mx]);               % fix the axes
  tumble(bb);                          % plot it
  return;
  
  % tumble until stopped with ^C
  function tumble(p)
    mx = max(abs(p(:)))*1.5;
    axis([-mx mx -mx mx]);             % fix the axes
    nd = size(p,2);
    a = rand(nd)/25;                   % about 1 degree
    for reps = 1:inf
      dr = ndrotate(a);
      for i=1:100                      % 100, then change direction
        cla;                           % clear previous
        fromInfinity;                  % new edges
        drawnow;
        p = p*dr;                      % new position
        pause(0.03);                   % leave some cycles 
      end
      a = a + (rand-0.5)/100;          % change direction
    end
  end

  % plot 2-D shadow of edges
  function fromInfinity                % nested  
    for k=numel(s):-1:1                % all edges
      e1 = [p(s(k),1)  p(f(k),1)];     % x ends
      e2 = [p(s(k),2)  p(f(k),2)];     % y end
      z = p(s(k),3) + p(f(k),3);       % 2*mx : -2*mx
      h = ((z+2*mz)/mz)/4;             %    1 : 0 
      h = 1-h;                         %    0 : 1
      c = clip([h h h]);               % black is nearest
      w = 2-h;
      plot(e1, e2, 'color', c, 'linewidth', w);
    end
  end

  % turn angles into orthogonal matrix
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
  end
end
