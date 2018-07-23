#!/usr/bin/python3
from __future__ import print_function
"""
frames.py
"""

import os
import sys

import rotate


def main(argv):
  num_frames = int(sys.argv[1])
  out_dir = sys.argv[2]

  with open('killeroo-frame.template') as f:
    t = f.read()

  center = [0, 63, -110]   # look at point from template
  orig_eye = [400, 20, 30]
  radius = rotate.distance(center, orig_eye)

  points = rotate.circle(center, radius, num_frames)

  for i in range(num_frames):
    p = {
      'eye_x': i * 0.1,
      'eye_y': 0.2,
      'eye_z': 0.3,
    }
    point = points[i]
    p = {
      'eye_x': point[0],
      'eye_y': point[1],
      'eye_z': point[2],
    }
    with open(os.path.join(out_dir, '%d.pbrt' % i), 'w') as f:
      print(t % p, file=f)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
