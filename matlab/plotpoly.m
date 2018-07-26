%PLOTPOLY plot 2-D projection of N-D polytope
%   PLOTPOLY(M) projects a matrix of vertices into a 2-D shadow of edges
%   PLOTPOLY(M, 'infinity') projects from infinity (default)
%   PLOTPOLY(M, 'nearby') projects from a closer point in space
%   PLOTPOLY(M, 'tumble') tumbles randomly and projects from infinity
%   M(i,:) is the coordinates of the i-th vertex.
%   Color and line width are used to show depth.
%

function plotpoly(p, flag)
  if nargin == 1 
    flag = 'infinity';                 % default
  end
  [s,f] = edges(p);                    % start,finish
  mz = max(abs(p(3,:)));               % z scale
  if size(p,2) >= 4; mw = max(abs(p(4,:))); end
  clip = @(vec) min(max(vec,0),1);     % black and white

  hold on
  axis equal
  axis off
  switch flag
    case 'infinity'
      fromInfinity;                    % display
    case 'nearby'
      fromNearby;                      % display
    case 'tumble'
      tumble;                          % display
      axis manual
  end
  hold off
  return;
    
  % tumble until stopped with ^C
  function tumble
    mx = max(abs(p(:)))*1.5;
    axis([-mx mx -mx mx]);             % fix the axes
    nd = size(p,2);
    a = rand(nd)/25;                   % about 1 degree
    for reps = 1:inf
      dr = ndrotate(a);
      for i=1:10
        cla;                           % clear previous
        fromInfinity;                  % new edges
        drawnow;
        p = p*dr;                      % new position
        pause(0.03);                   % leave some cycles 
      end
      a = a + (rand-0.5)/100;          % change direction
    end
  end
    
  % a function to plot 2-D shadow of edges
  function fromInfinity                % nested  
    for k=numel(s):-1:1                % all edges
      e1 = [p(s(k),1)  p(f(k),1)];     % x ends
      e2 = [p(s(k),2)  p(f(k),2)];     % y ends
      if size(p,2) == 3                % 3-D figures
        z = p(s(k),3) + p(f(k),3);     % 2*mx : -2*mx
        h = ((z+2*mz)/mz)/4;           %    1 : 0 
        h = 1-h;                       %    0 : 1
        c = clip([h h h]);             % black is nearest
        w = 2-h;
      else                             % 4-D figures
        z  = p(s(k),3) + p(f(k),3);    % 2*mx to -2*mx dim=3
        w  = p(s(k),4) + p(f(k),4);    % 2*mx to -2*mx dim=4
        h1 = ((z+2*mz)/mz)/4;          %   1 : 0
        h2 = 1-h1;                     %   0 : 1
        h3 = ((w+2*mw)/mw)/4;          %   1 : 0
        c = clip(1.2*[h1*.9 .4*h3 h2]);
        w = 1;
      end
      plot(e1, e2, 'color', c, 'linewidth', w);
    end
  end

  % a function to plot 2-D shadow of edges
  function fromNearby                  % nested  
    hold on                            % plot it
    axis equal
    nearby = mx+.1;
    toscreen = 40;
    for k=1:numel(s)                   % all edges
      y = [p(s(k),1)  p(f(k),1)];      % x ends
      z = [p(s(k),2)  p(f(k),2)];      % y ends
      x = [p(s(k),3)  p(f(k),3)];      % z ends
      sx = x.*toscreen./(nearby-z);
      sy = y.*toscreen./(nearby-z);
      plot(sx, sy);
    end
    hold off
  end
end
