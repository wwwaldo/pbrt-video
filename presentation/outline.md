Hyperdodecahedron in a Bathroom
===============================

This repository contains code and data to render a video using [PBRT][]!  It
was done [Recurse Center][] by Caroline Lin and Andy Chu.

[PBRT]: http://www.pbrt.org/
[Recurse Center]: https://recurse.com

<!-- TODO: screenshot of video -->

Components
----------

    $ ./count.sh code  # an overview of relevant code / data

- ~900 lines of our own Python code
- ~200 lines in [schlafli_interpreter.py][] from `aruth2`
- Libraries used
  - NumPy for linear algebra
  - SciPy for convex hull algorithm
  - matplotlib for plotting the prototypes
- Tools used:
  - PBRT for rendering
  - ImageMagick for resizing frames, joining frames to video
  - Meshlab (a GUI tool) for combining the polytope with the bathroom scene
- ~500 lines of shell
  - Coordinating Python, PBRT, ImageMagick, etc.
  - Running rendering over 3 machines
    - Rendering time: 4-8 hours on 33 cores/66 hyperthreads over 3 Heap
      machines
    - mod-sharding with shell scripts!
  - ssh, rsync
  - xargs -P for resizing frames in parallel
- ~5800 lines of textual PBRT description for bathroom
  - 19 MB geometry
  - 14 MB textures
  - 21 MB blend file?
  - Sky environment map (imgtool)

[schlafli_interpreter.py]: https://github.com/aruth2/schlafli/blob/master/schlafli_interpreter.py

Influences / Prior Art
----------------------

- Bathsheba
- 4D Toys, Miegakure (120 cell)
- Flatland, etc.

TODO: What's the best explanation of 4D?  Extruding 2D to 3D
  1978 video
  numberphile video

Algorithm
---------

1. Use [schlafli_interpreter.py][] to generate a polytope.  It takes a
   Schlafli symbol -- like `{5,3,3}` for the hyperdodecahedron aka 120-cell --
   and generates algorithm to generate vertices, edges, faces, hyperfaces,
   etc.  There is general recursive algorithm to do this.  The base case of
   the recursion is dimension 1, so you make 4 calls to get to dimension 4.
2. Intersect the edges of the polytope with a hyperplane (a 3D subset of 4D).
3. You get a set of 3D points out of step 2. Draw the convex hull of them,
   which gives you triangles.
4. Render the triangles somehow.  We used both matplotlib's 3d facilities
   (mplot3d) and [PBRT][].
5. Animate over different hyperplanes. Take the min and max along the w axis
   and that will give you non-empty slices. Now you can "see" the 4D polytope
   using time as the 4th dimension.

Also:

- Rotate the camera
- Rotate the polytope

[schlafli]: https://github.com/aruth2/schlafli

Original comment: https://news.ycombinator.com/item?id=17687033

Pipeline
--------

1. Export a `.pbrt` file per frame.
2. Distribute code, data, and configuration to 3 machines with rsync
3. Render to PNG with PBRT running under tmux (so we don't lose the sessions).
4. Copy frames back with rsync.
5. Resize frames and join to video with ImageMagick.

Things We Learned About
-----------------------

- Geometry
  - Schlafli symbol representation of polytopes in arbitrary dimensions.
  - v-polytope vs. h-polytope 
    - Convex Hull gives you the h-polytope from the v-polytope (roughly).
- Linear Algebra:
  - for line segment-plane intersection (this generalized from 3D to 4D
    easily, so we didn't need to do anything special)
  - rotations in 3D and 4D
- Raytracing -- tuning the sample and size parameters
- File formats
  - PLY mesh format
  - EXR image format
- Tools
  - matplotlib: mplot3d and animations
  - ipython3 (hadn't used it before)

Possible Future Directions
--------------------------

- More polytopes in more scenes
- Automation could be improved / more foolproof.  Reduce manual work.

Maybe:

- Interactive polytopes in the browser (look at existing implementations)
- Android filament: real-time rendering?

Future Research:

- How does the Schlafli generator work, exactly?
- How does Convex Hull work?  SciPy uses http://www.qhull.org .

Credits
-------

- `contemporary-bathroom` scene from http://pbrt.org/scenes-v3.html

> Scene thanks to Mareck. CC-Zero (public domain) license.
> "contemporary_china" texture used for wallpaper thanks to Adam Charlts;
> texture contrast was increased for the render. "American_walnut_pxr128" wood
> texture courtesy Pixar Animation Studios, CC-BY license. Abstract print seen
> in mirror based on a smoke photograph by Vanessa Pike-Russell, CC-BY
> license; the photo was inverted and contrast was adjusted for rendering.
> Hurricane image used for photo on wall courtesy NASA Goddard Space Flight
> Center, CC-BY license.

- `aruth2` for [schlafli_interpreter.py][]

