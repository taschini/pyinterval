# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

class app(object):

    def __init__(self, doctests = None, docfiles = None):
        self.doctests = doctests or []
        self.docfiles = docfiles or []

    def _import(self, name):
        m = __import__(name)
        for c in name.split('.')[1:]:
            m = getattr(m, c)
        return m

    def suite(self):
        import unittest, doctest, glob
        import os.path as op
        s = unittest.TestLoader().loadTestsFromModule(__import__(self.__module__))
        prefix = op.dirname(__file__)
        names = [m[len(prefix)+1:-3] for m in glob.glob(op.join(prefix, 'test*.py'))]
        for m in names:
            s.addTest(unittest.TestLoader().loadTestsFromModule(self._import('test.' + m)))
        for m in self.doctests:
            try:
                m = self._import(m)
            except ImportError:
                pass
            else:
                s.addTest(doctest.DocTestSuite(m))
        s.addTest(doctest.DocFileSuite(module_relative=False, *self.docfiles))
        return s

    def parse_cli(self, argv):
        import optparse
        parser = optparse.OptionParser(prog=argv[0])
        parser.set_defaults(verbosity=[1])
        parser.add_option("-v", "--verbose", dest='verbosity', action='append_const', const=+1, help="increase verbosity")
        parser.add_option("-q", "--quiet",   dest='verbosity', action='append_const', const=-1, help="decrease verbosity")
        parser.add_option("-n", "--names",   action='store_true', help="show test names instead of descriptions", default=False)
        return parser.parse_args(argv[1:])

    def main(self, argv=None):
        import sys
        (options, args) = self.parse_cli(argv or sys.argv)
        import unittest
        if args:
            import re
            s = unittest.TestSuite()
            all = self.suite()
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
            s = self.suite()
        return not unittest.TextTestRunner(verbosity=sum(options.verbosity), descriptions=not options.names).run(s).wasSuccessful()


if __name__ == '__main__':
    import sys
    sys.exit(app().main(sys.argv))

