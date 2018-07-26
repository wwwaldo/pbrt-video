% FILE:    vertices.m
% PURPOSE: mXn array of vertices for named polytopes
%          center on the origin with unit edge
% NAMES:   nnntttt where nnn is the number of ttt is unambiguous
% name Schlafli   popular
% 3edge   s3   (triangle)
% 5edge   s5   (pentagon)
% 4face   s34  tetrahedron (start of simplex series)
% 6face   s43  cube        (start of measure series)
% 8face   s34  octahedron  (start of cross series)
% 12face  s53  dodecahedron
% 20face  s35  icosahedron
% 5cell   s333 hypertetrahedron (4-simplex)
% 16cell  s334 hyperoctahedron  (4-cross)
% 8cell   s433 hypercube        (4-measure)
% 24cell  s343 (unique and nameless)
% 120cell s533 hyperdodecahedron
% 600cell s355 hypericosahedron

function v = vertices(varargin)

  if nargin == 1                       % figure name
    name = varargin{1};
  elseif nargin == 2                   % d,nf description
    switch varargin{1}
      case {2, '2'}, bound = 'edge';
      case {3, '3'}, bound = 'face';
      case {4, '4'}, bound = 'cell';
      otherwise, error('no such dimension');
    end
    count = varargin{2};
    if ~ischar(count), count = num2str(count); end
    name = [count bound];
  end
  
  if numel(name) > 4 && strcmp(name(end-3:end), 'edge')
    vct = str2double(name(1:end-4));     % polygon
    a = 2*pi*(1:vct)/vct;
    v = [sin(a); cos(a)]';
    e = v(1,:) - v(2,:);                 % an edge
    v = v/sqrt(e*e');                    % unit edges
  else
    r2 = sqrt(2);
    r5 = sqrt(5);
    gr = (1+r5)/2;                       % golden ratio
    switch name
      
    case {'4face', 'tetrahedron', 's33', '3simplex'}
      v = perms([1 0 0 0]/r2, 'cycles');
    case {'6face', 'cube', 's43', '3measure'}
      v = perms([1 1 1]/2, 'signs');
    case {'8face', 'octahedron', 's34', '3cross'}
      v = perms([1 0 0]/r2, 'cycles', 'signs', 'unique');
    case {'12face', 'dodecahedron', 's53'}
      v1 = perms([0 1 gr^2], 'cycles');
      v = perms([v1; [1 1 1]*gr]/2, 'signs', 'unique');
    case {'20face', 'icosahedron', 's35'}
      v = perms([1 0 gr]/2, 'cycles', 'signs', 'unique');
      
    case {'5cell', 'hypertetrahedron', 's333', '4simplex'}
      v = perms([1 0 0 0 0]/r2, 'cycles');
    case {'8cell', 'hypercube', 's433', '4measure'}
      v = perms([1 1 1 1]/2, 'signs');
    case {'16cell', 'hyperoctahedron', 's334', '4cross'}
      v = perms([1 0 0 0]/r2, 'cycles', 'signs', 'unique');
    case {'24cell', 's343'}
      v = perms([1 1 0 0]/r2, 'signs', 'all', 'unique');   % 24 cell
    case {'120cell', 'hyperdodecahedron', 's533'}
      vs1 = perms([...
        2    2     0     0; 
       r5    1     1     1; 
       gr    gr    gr    gr^-2; 
       gr^2  gr^-1 gr^-1 gr^-1], 'unique');
      vs2 = perms([...
       gr^2  gr^-2 1     0; 
       r5    gr^-1 gr    0; 
       2     1     gr    gr^-1], 'even');
      v = perms([vs1; vs2]*gr^2/2, 'signs', 'unique');   % 120 cell 
    case {'600cell', 'hypericosahedron', 's335'}
      vs1 = perms([2 0 0 0; 1 1 1 1], 'cycles');
      vs2 = perms([gr 1 gr^-1 0], 'even');
      v = perms([vs1; vs2]*gr/2, 'signs', 'unique');     % 600 cell
    otherwise,
      error(['bad input ' name]);
    end
  end


