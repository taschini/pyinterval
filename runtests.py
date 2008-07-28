#! /usr/bin/env python

# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.


def main(argv = None):
    import test, glob
    import os.path as op
    return test.app(doctests=['interval', 'test.helpers'], docfiles=glob.glob(op.join(op.dirname(__file__), 'doc', '*.rst'))).main(argv)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

