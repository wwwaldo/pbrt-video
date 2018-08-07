#!/usr/bin/python3
import sys
import argparse

# Generate a partially completed template for further processing by run.sh.
# Fills in main performance.
def _bathroom_settings(resolution_x, resolution_y, sobol_pixelsamples, 
    bdpt_integrator_depth, template_path=None, out=None):
    template_path = template_path or 'bathroom-base.template'
    out = out or 'bathroom.template'
    
    with open(template_path) as file:
        header = file.read()
    macro_replacements = {
        'resolution_x' : resolution_x,
        'resolution_y' : resolution_y, 
        'sobol_pixelsamples' : sobol_pixelsamples,
        'bdpt_integrator_depth' : bdpt_integrator_depth,
        'out_filename' : '%(out_filename)s',
        'ply_filename' : '%(ply_filename)s'
    }
    
    with open(out, 'w') as outf:
        print(header % macro_replacements, file=outf)


def main(argv):
    parser = argparse.ArgumentParser(description='Tweak quality settings for bathroom scene.')
    parser.add_argument('--resx', type=int, help='num pixels for x-coordinate')
    parser.add_argument('--resy', type=int, help='num pixels for y-coordinate')
    parser.add_argument('--nsamples', type=int, help='num samples per ray for sobol integrator')
    parser.add_argument('--depth', type=int, help='max depth per ray for integrator')
    parser.add_argument('--fname', type=str, help='template name')
    args = parser.parse_args(argv[1:])
    _bathroom_settings(args.resx, args.resy, args.nsamples, args.depth, template_path=args.fname)
    return

if __name__ == "__main__":
    main(sys.argv)
