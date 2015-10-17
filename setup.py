#! /usr/bin/env python

# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

"""Script for setting the distribution of the interval package and the
crlibm extension.

Typical usage
-------------

Build crlibm and place it in the current directory:

    python setup.py build_ext -i


Create a source distribution:

    python setup.py sdist --formats=gztar,zip

"""


try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from distutils.command.build_py import build_py

class custom_build_py(build_py):
    def run(self):
	from os import path as op
        def fix(package, src_dir, build_dir, filenames):
            assert filenames == [op.join('..', 'LICENSE')]
            return (package, '.', build_dir, ['LICENSE'])
        self.data_files = [fix(*t) for t in self.data_files]
        return build_py.run(self)

# A subset of http://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Mathematics'
]

metadata = dict(
    description  = 'Interval arithmetic in Python',
    author       = 'Stefano Taschini',
    author_email = 'taschini@gmail.com',
    url          = "https://github.com/taschini/pyinterval",
    classifiers  = classifiers
);

description="""
This library provides a Python implementation of an algebraically
closed interval system on the extended real number set. An interval
object consists of a finite union of closed, possibly unbound,
mathematical intervals.

Installation
------------

The most convenient way to install this library is by means of `easy_install`_::

    easy_install pyinterval

Alternatively, it is possible to download the sources from PyPI_ and invoking ::

    python setup.py install

in the unpacked directory. Note that you need the crlibm_ library
installed on your system. It is also possible to retrieve the source code
from the GitHub `repository`_.

.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pypi: http://pypi.python.org/pypi/pyinterval/
.. _crlibm: http://lipforge.ens-lyon.fr/www/crlibm/
.. _repository: https://github.com/taschini/pyinterval

Documentation
-------------

Full documentation is available at
http://cdn.rawgit.com/taschini/pyinterval/master/html/index.html
"""

setup(
    name         = 'pyinterval',
    version      = '1.0b21',
    packages     = ['interval'],
    package_data = dict(interval=['../LICENSE']),
    cmdclass     = dict(build_py=custom_build_py),
    ext_modules  = [
        Extension(
            'crlibm',
            sources      = ['ext/crlibmmodule.c'],
            include_dirs = ['/opt/crlibm/include'],
            library_dirs = ['/opt/crlibm/lib'],
            libraries    = ['crlibm'])
        ],
    long_description = description,
    **metadata)
