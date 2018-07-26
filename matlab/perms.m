%PERMS all different permutations of matrix rows
%   PERMS(M) extends mXn matrix M to one containing all permutations of
%   values for each row.
%   PERMS(M)           gives all permutations (default).
%
%   Flags:
%   PERMS(M, 'even')   gives even permutations.
%   PERMS(M, 'odd')    gives odd permutations.
%   PERMS(M, 'all')    gives all permutations (default).
%   PERMS(M, 'cycles') gives all end-around shifts.
%   PERMS(M, 'signs')  gives all changes of sign.
%   PERMS(M, 'unique') sorts the result and removes repeated rows.
%   Flags 'signs' and/or 'unique' can be used with other flags.
%   Flags 'all', 'even', 'odd' and 'cycles' are mutually exclusive.
%   class(M) is the same as class(perms(M, flags)).
%   The result of perms is acceptable input to another call of perms.
%   perms 'unique' is idempotent.  I.e.,
%      t = perms(M, flag, 'unique') is the same as
%      t = perms(t, flag, 'unique')
%   Flag 'unique' is computationally expensive.  Avoid it if you can.
%   PERMS is memory limited.  When the application permits it, use a
%   smaller input data type (such as int8).
%
%   Examples: 
%      perms(1:2) is              [1 2; 2 1]
%      perms(1:3, 'even') is      [3 1 2; 1 2 3; 2 3 1]
%      perms((1:3)/2, 'odd') is   [1.5 1.0 0.5; 0.5 1.5 1.0; 1.0 0.5 1.5]
%      perms(1:2, 'signs') is     [-1 -2; -1 2; 1 -2; 1 2]
%      perms([1 0 0],'unique') is [0 0 1; 0 1 0; 1 0 0]
%      perms([1 1; 2 1]) is       [1 1; 1 2; 2 1]
%      perms('abc', 'cycles') is  ['abc'; 'cab'; 'bca']
%
%   Class support for input M:
%      numeric, sparse, char, logical, complex
%   Note: the 'signs' flag can be applied to all numeric classes
%   except unsigned ints and (temporarily) 64-bit ints.
%
%   See also RANDPERM NCHOOSEK

function M = perms(M, varargin)        % outer function
  % get input bounds
  if numel(M) == 0, return; end
  if ndims(M) ~= 2,
    error('MATLAB:perms:input', 'requires mXn input');
  end

  % process flags
  fPerm=1; fOdd=2; fEven=3; fCycle=4; fSign=5; fUnique=6;
  opt = false(1,6);
  for arg = 1:nargin-1
    switch lower(varargin{arg})
      case 'all',    opt(fPerm)   = true;
      case 'odd',    opt(fOdd)    = true;
      case 'even',   opt(fEven)   = true;
      case 'cycles', opt(fCycle)  = true;
      case 'signs',  opt(fSign)   = true;
      case 'unique', opt(fUnique) = true;
      otherwise, error('MATLAB:perms:badflag', 'unknown flag');
    end
  end
  if ~any(opt(fPerm:fSign)); opt(fPerm) = true; end % default

  % avoid meaningless combinations of flags
  if sum(opt(fPerm:fCycle)) > 1
    error('MATLAB:perms:badflag', 'conflicting flags');
  end
  
  % compute basic permutations, result in M
  [nr, nc] = size(M);                  % input vectors
  if     opt(fPerm),  allPerms(fPerm);
  elseif opt(fOdd),   allPerms(fOdd);
  elseif opt(fEven),  allPerms(fEven);
  elseif opt(fCycle), allCycles;
  end

  % compute all sign variations
  [nr, nc] = size(M);                  % might have changed
  if     opt(fSign),  allSigns; end

  % discard repeated entries, get canonical order
  if opt(fUnique), M = unique(M, 'rows'); end
  return                               % that's all folks
  %--------- end of execution in main function --------------------
  
  function allPerms(flag)              % nesting level 1
    % temporarily make types numeric
    if islogical(M),  w = uint8(M);
    elseif ischar(M), w = uint16(M);
    else              w = M;
    end
    % permute 1:nc
    if flag == fPerm,    
      makePerms; q = pa{nc};
    else
      makeEvenOdd;
      if flag == fOdd, q = odd{nc}; else q = even{nc}; end
    end
    md = size(q,1);
    
    % do the work
    res = zeros(md*nr, nc, class(w));    % place for result
    for i=1:nr
      z = w(i,:);                        % one vector at a time
      res((i-1)*md+1:i*md, :) = z(q);    % permuted i-th input
    end

    % cleanup and deliver result
    if islogical(M),    M = logical(res); 
    elseif ischar(M),   M = char(res);
    elseif issparse(M), M = sparse(res);  
    else                M = res;         % result in M
    end
    return;                              % from allPerms
    % ----------- end of execution in allPerms --------------------
    
    % Build up standard permutation matrices: These matrices are always the
    % same (permutations of 1:n) for any data. The permutation matrices are
    % class uint8 to save storage.
    function makePerms                   % nesting level 2
      pa = {1};                          % all perms, res in pa{}
      for i = 2:nc                       % the rest
        c = pa{i-1};
        [bh, bw] = size(c);              % block height & width
        o  = ones(bh, 1, 'uint8');
        nh = bh*i;                       % new height
        nw = bw+1;                       % new width
        b = zeros(nh, nw, 'uint8');      % new block

        b(1:bh, :) = [i*o, c];           % just a copy
        for j=1:i-1
          d = c;
          d(c==j) = i;                   % substitute i for j
          b(j*bh+1:(j+1)*bh, :) = [j*o, d];
        end
        pa{end+1} = b;
      end
      return;                            % from makePerms
    end
    % -------------------  end makePerms ----------------------
    
    % Build up even and odd permutation matrices:  These matrices are always
    % the same for any input data.  The class is uint8 to save storage.
    function makeEvenOdd               % nesting level 2
      even{1} = uint8(1);              % res in even{}, odd{}
      odd{1}  = uint8(1);
      even{2} = uint8([1 2]);
      odd{2}  = uint8([2 1]);
      for i=3:nc
        od = odd{i-1};
        ev = even{i-1};
        [bh, bw] = size(od);
        o = ones(bh, 1, 'uint8');
        z = zeros(bh*i, bw+1, 'uint8');% new block
        td = z;
        te = z;

        td(1:bh,:) = [i*o, od];        % just extend odd
        te(1:bh,:) = [i*o, ev];        % just extend even

        for j=1:i-1
          t = ev;                      % for new odd
          t(ev==j) = i;                % substitute i for j
          td(j*bh+1:(j+1)*bh, :) = [j*o, t];
          t = od;                      % for new even
          t(od==j) = i;                % substitute i for j
          te(j*bh+1:(j+1)*bh, :) = [j*o, t];
        end
        odd{end+1}  = td;              % save for later use
        even{end+1} = te;
      end
      return;                          % from makeEvenOdd
    end
    % ------------------ end makeEvenOdd ---------------------
  end
  % --------------------- end allPerms -----------------------------
  
  function allCycles                   % nesting level 1
    md = nc;
    mr = nr*md;

    % force numeric type for zeros()
    if     ischar(M),    w = uint16(M);
    elseif islogical(M), w = uint8(M);
    else                 w = M;
    end
    res = zeros(mr, nc, class(w));     % preallocate result

    % do the work
    for i=1:nr
      s = 1+(i-1)*md;
      bl = s:i*md;
      res(bl,1:nc) = repmat(w(i,:), md, 1);
      for r = s+1:s+nc-1
        res(r, [2:end, 1]) = res(r-1, :);  % end around
      end
    end

    % restore input type
    if islogical(M),    M = logical(res);
    elseif ischar(M),   M = char(res);
    elseif issparse(M), M = sparse(res);
    else                M = res;
    end
    return;                            % from allcycles
  end
  % ----------------- end allcycles ----------------------------
  
  function allSigns                    % nesting level 1
    if ~isnumeric(M)
      error('MATLAB:perms:signs', 'requires numeric argument');
    end
    r = class(M);
    if r(1) == 'u' 
      error('MATLAB:perms:signedarg', 'requires signed argument');
    end

    md = 2^nc;                         % all signs
    mr = nr*md;                        % result size

    % allocate result
    p = zeros(mr, nc, class(M));       % worst case
    
    % do the work
    for i=1:nr                         % one input row at a time
      tmp = repmat(M(i,:), md, 1);     % block of data
      step = md;
      for j=1:nc                       % for each column
        sgn = 1;
        step = step/2;
        rep  = md/step;
        for k = 0:rep-1                % for each block
          sgn = -sgn;
          for m = 1:step
            row = k*step+m;
            tmp(row,j) = sgn*tmp(row,j);
          end
        end
      end
      p(md*(i-1)+1:i*md,:) = tmp;
    end
    M = p;                             % report result
  end
  % ----------------------- end allSigns ----------------

end
%------------------------ end perms ------------------  
  
  