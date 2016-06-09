# Copyright (c) 2008-2016, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.


def additional_tests():
    import doctest
    import glob
    import interval
    import os
    import unittest
    from . import helpers

    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(interval))
    s.addTest(doctest.DocTestSuite(helpers))

    docfiles = glob.glob(os.path.join(os.path.dirname(__file__), '..', '*', '*.rst'))
    s.addTest(doctest.DocFileSuite(module_relative=False, *docfiles))
    return s
