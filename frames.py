#!/usr/bin/python3
from __future__ import print_function
"""
frames.py
"""

import os
import sys


def main(argv):
  num_frames = int(sys.argv[1])
  out_dir = sys.argv[2]

  with open('killeroo-frame.template') as f:
    t = f.read()

  for i in range(num_frames):
    with open(os.path.join(out_dir, '%d.pbrt' % i), 'w') as f:
      print(t % {
        'eye_x': i * 0.1,
        'eye_y': 0.2,
        'eye_z': 0.3,
      }, file=f)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
