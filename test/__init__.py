# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

def additional_tests():
    import unittest, doctest, sys, os, glob
    s = unittest.TestSuite()
    for m in ['interval', 'test.helpers']:
        try:
            __import__(m)
            m = sys.modules[m]
        except ImportError:
            pass
        else:
            s.addTest(doctest.DocTestSuite(m))

    docfiles = glob.glob(os.path.join(os.path.dirname(__file__), '..', '*', '*.rst'))
    s.addTest(doctest.DocFileSuite(module_relative=False, *docfiles))
    return s
