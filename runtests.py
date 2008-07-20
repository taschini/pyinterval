#! /usr/bin/env python

# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

import unittest, doctest, glob


def suite():
    module = __import__(suite.__module__)
    s = unittest.TestLoader().loadTestsFromModule(module)
    for m in 'interval', 'fpu', 'helpers', 'test', 'test_extra':
        try:
            m = __import__(m)
        except ImportError:
            pass
        else:
            s.addTest(unittest.TestLoader().loadTestsFromModule(m))
            try:
                s.addTest(doctest.DocTestSuite(m))
            except:
                pass
    s.addTest(doctest.DocFileSuite(*glob.glob('doc/*.rst')))
    return s


def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv
    import optparse
    parser = optparse.OptionParser(prog=argv[0])
    parser.set_defaults(verbosity=[1])
    parser.add_option("-v", "--verbose", dest='verbosity', action='append_const', const=+1, help="increase verbosity")
    parser.add_option("-q", "--quiet",   dest='verbosity', action='append_const', const=-1, help="decrease verbosity")
    parser.add_option("-n", "--names",   action='store_true', help="show test names instead of descriptions", default=False)
    (options, args) = parser.parse_args(argv[1:])
    if args:
        import re
        s = unittest.TestSuite()
        all = suite()
        def visit(n, p):
            try:
                for c in n:
                    visit(c, p)
            except:
                if p.search(n.id()):
                    s.addTest(n)
        for p in args:
            visit(all, re.compile(p))
    else:
        s = suite()
    return not unittest.TextTestRunner(verbosity=sum(options.verbosity), descriptions=not options.names).run(s).wasSuccessful()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

