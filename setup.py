#! /usr/bin/env python

# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

version = '1.0.1.dev0'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# A subset of http://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Mathematics'
]

@apply
def long_description():
    with open('README.rst') as f:
        return f.read().decode('utf8')

metadata = dict(
    author           = 'Stefano Taschini',
    author_email     = 'taschini@gmail.com',
    classifiers      = classifiers,
    description      = 'Interval arithmetic in Python',
    license          = 'BSD',
    long_description = long_description,
    platforms        = '',
    url              = "https://github.com/taschini/pyinterval",
);

data                 = dict(
    name             = 'pyinterval',
    version          = version,
    packages         = ['interval'],
    package_data     = dict(interval=['LICENSE']),
    # install_requires = ['crlibm~=1.0'],  this is till too new to be broadly supported.
    install_requires = ['crlibm>=1.0,==1'],
    test_suite       = 'test',
    tests_require    = [],
    **metadata)

if __name__ == '__main__':
    setup(**data)
