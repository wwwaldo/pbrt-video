Hyperdodecahedron in a Bathroom
===============================

This repository contains code and data to render a video using [PBRT][]!  It
was done at [Recurse Center][] by Caroline Lin and Andy Chu.

[PBRT]: http://www.pbrt.org/
[Recurse Center]: https://recurse.com

Screenshots
-----------

We prototyped the geometry with NumPy and matplotlib, and then rendered it
with PBRT.

![Wireframe of Hyperdodecahedron][wireframe-120]

![Rendered Screenshot][rendered-120]

[wireframe-120]: https://raw.githubusercontent.com/caroline-lin/pbrt-video/master/media/5-3-3__frame002.small.png

[rendered-120]: https://raw.githubusercontent.com/caroline-lin/pbrt-video/master/media/frame050.small.png

See the Full Video
------------------

[10 second video of a Hyperdodecahedron in a Bathroom][120-cell-bathroom] (2.8 MB) ([mirror][120-cell-mirror])

[120-cell-bathroom]: http://www.oilshell.org/recurse/120-cell-bathroom.original.html
[120-cell-mirror]: https://andychu.github.io/recurse/120-cell-bathroom.mirror.html

Components
----------

    $ ./count.sh code  # an overview of relevant code / data

- ~900 lines of our own Python code
- ~200 lines in [schlafli_interpreter.py][] from `aruth2`
- Libraries used
  - [NumPy][] for linear algebra
  - [SciPy][] for the convex hull algorithm
  - [matplotlib][] for plotting the prototypes
- Tools used:
  - [PBRT][] for rendering
  - [ImageMagick][] for resizing frames
  - [ffmpeg][] for encoding frames to video
  - [MeshLab][] (a GUI tool) for combining the polytope with the bathroom scene
- ~500 lines of shell scripts (more motivation for [Oil shell](http://www.oilshell.org/))
  - To coordinate Python code and the tools above
  - To render across 3 machines
    - Rendering time: 4-8 hours on 33 cores/66 hyperthreads across 3 Heap
      machines
    - mod-sharding with shell scripts!
  - `ssh`, `rsync` to distribute inputs and collect outputs
  - `xargs -P` for resizing frames in parallel
- ~5800 lines of textual PBRT description for bathroom
  - 19 MB geometry
  - 14 MB textures
  - 21 MB blend file?
  - Sky environment map (imgtool)

[schlafli_interpreter.py]: https://github.com/aruth2/schlafli/blob/master/schlafli_interpreter.py

[NumPy]: http://www.numpy.org/
[SciPy]: https://www.scipy.org/
[matplotlib]: https://matplotlib.org/

[ImageMagick]: https://www.imagemagick.org/script/index.php
[ffmpeg]: https://www.ffmpeg.org/
[MeshLab]: http://www.meshlab.net/

Influences / Prior Art
----------------------

- [4D Toys](http://4dtoys.com/), [Miegakure](http://miegakure.com/)
- [Bathsheba Grossman](https://bathsheba.com/sculpt/) -- making mathematical
  objects real!

Stuff Andy was fascinated by 15+ years ago!

- [HyperSpace Polytope Slicer](http://dogfeathers.com/java/hyperslice.html)
  (not sure if the Java Applet still works)
- [Russell Towle's 4D Star Polytope Animations](http://dogfeathers.com/towle/star.html)

Algorithm
---------

1. Use [schlafli_interpreter.py][] to generate a polytope.  It takes a
   Schlafli symbol -- like `{5,3,3}` for the hyperdodecahedron aka
   [120-cell][] -- and generates algorithm to generate vertices, edges, faces,
   hyperfaces, etc.  There is general recursive algorithm to do this.  The
   base case of the recursion is dimension 1, so you make 4 calls to get to
   dimension 4.
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

[120-cell]: https://bathsheba.com/sculpt/

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
- Rotation about different axes (in 4D too).  Look at the Polytope slicer
  applet again.

Maybe:

- Interactive polytopes in the browser (look at existing implementations)
- Android filament: real-time rendering?

Future Research:

- How does the Schlafli generator work, exactly?
- How does Convex Hull work?  SciPy uses http://www.qhull.org .
- How to obtain triangles for star polytopes?  Taking the Convex hull won't
  work in this case.

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

