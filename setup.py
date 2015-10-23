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

version = '1.0.0'

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from distutils.command.build_py import build_py
from distutils.command.build_ext import build_ext
from distutils import cygwinccompiler

class Msys2CCompiler (cygwinccompiler.CygwinCCompiler):
    # From https://github.com/aleaxit/gmpy/blob/ff2a8cca8e6f6901aa8ebb7e56a5fb19b236aaf0/msys2_build.txt

    compiler_type = 'msys2'

    def __init__ (self,
                  verbose=0,
                  dry_run=0,
                  force=0):

        cygwinccompiler.CygwinCCompiler.__init__ (self, verbose, dry_run, force)
        shared_option = "-shared" if self.ld_version >= "2.13" else "-mdll -static"
        entry_point = '--entry _DllMain@12' if self.gcc_version <= "2.91.57" else ''
        common_flags = ' -O2 -Wall -fno-strict-aliasing -fwrapv'
        import sys
        if sys.maxsize > 2**32:
            common_flags += ' -DMS_WIN64'
        self.set_executables(compiler     = 'gcc'       + common_flags,
                             compiler_so  = 'gcc -mdll' + common_flags,
                             compiler_cxx = 'g++'       + common_flags,
                             linker_exe='gcc',
                             linker_so='%s %s %s' % (self.linker_dll, shared_option, entry_point))
        self.dll_libraries=[]

@apply
def register_msys2ccompiler():
    from distutils.ccompiler import compiler_class
    cygwinccompiler.Msys2CCompiler = Msys2CCompiler
    compiler_class['msys2'] = ('cygwinccompiler', 'Msys2CCompiler', "MSYS2/MinGW-w64 port of GNU C Compiler for MS Windows")
    return 'Done'

class custom_build_py(build_py):
    # Copy the license file into the package directory
    def run(self):
        from os import path as op
        def fix(package, src_dir, build_dir, filenames):
            assert filenames == [op.join('..', 'LICENSE')]
            return (package, '.', build_dir, ['LICENSE'])
        self.data_files = [fix(*t) for t in self.data_files]
        return build_py.run(self)

class custom_build_ext(build_ext):
    """Build C/C++ extensions, without aborting in case of failure."""

    def make_dependencies(self):
        import subprocess as sub
        sub.call('make -C deps'.split())

    def run(self):
        try:
            build_ext.run(self)
        except Exception as ex:
            import sys
            sys.stderr.write("*** Could not build any of the extensions: {!r}\n*** Skipping...\n".format(ex))

    def build_extension(self, ext):
        for attempt in range(2):
            try:
                return build_ext.build_extension(self, ext)
            except Exception as ex:
                if attempt == 0:
                    self.make_dependencies()
        import sys
        sys.stderr.write("*** Could not build the extension {!r}: {!r}\n*** Skipping...\n".format(ext.name, ex))


# A subset of http://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: BSD License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: CPython',
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
    download_url     = "https://github.com/taschini/pyinterval/archive/{}.tar.gz".format(version),
    url              = "https://github.com/taschini/pyinterval",
);

data = dict(
    name          = 'pyinterval',
    version       = version,
    packages      = ['interval'],
    package_data  = dict(interval=['../LICENSE']),
    cmdclass      = dict(build_py=custom_build_py, build_ext=custom_build_ext),
    test_suite    = 'test',
    ext_modules   = [
        Extension(
            'crlibm',
            sources      = ['ext/crlibmmodule.c'],
            include_dirs = ['deps/build/include'],
            library_dirs = ['deps/build/lib'],
            libraries    = ['crlibm'])
        ],
    **metadata)

if __name__ == '__main__':
    setup(**data)
