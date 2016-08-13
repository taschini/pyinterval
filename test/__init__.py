# Copyright (c) 2008-2016, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.


def additional_tests():
    # Invoked by setuptools when running "setup.py test"
    import doctest
    import glob
    import interval
    import os
    import unittest
    from . import helpers

    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(interval))
    s.addTest(doctest.DocTestSuite(helpers))

    # On Python >= 2.7 the repr of floats has been improved.  We test
    # the examples in the narrative docs only with Python versions
    # having the new repr.
    if repr(1/3.0) == '0.3333333333333333':
        docfiles = glob.glob(os.path.join(os.path.dirname(__file__), '..', '*', '*.rst'))
        s.addTest(doctest.DocFileSuite(module_relative=False, *docfiles))
    return s
