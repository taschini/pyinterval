Installation
============

The most convenient way to install this library is with `pip <https://pip.pypa.io>`_::

    pip install pyinterval

Note that if no binary distributions for your platform are available
on PyPI_, you need to ensure that the `crlibm
<http://lipforge.ens-lyon.fr/www/crlibm/>`_ library be installed on
your system.

Installing from sources on Linux and OS X
-----------------------------------------

You can either download the sources from PyPI_ or clone the repository
hosted on `GitHub <https://pypi.python.org/pypi/pyinterval/>`_::

    git clone https://github.com/taschini/pyinterval.git

To download and compile the dependencies::

    make -C deps

Finally, to compile and install this library::

    python setup.py install

Installing from sources on MS Windows
-------------------------------------

To compile PyInterval and its dependencies you need an MSYS2
environment with MinGW-w64. Once you obtained the sources as you would
on Linux or OS X, you set up the following environment variables:

===========  ==================================================
Variable     Description
===========  ==================================================
PYTHON       The installation directory of Python
PYTHON_ARCH  32 or 64 (bits), depending on the installed Python
PYTHON_DLL   The path to the Python DLL library
===========  ==================================================

Next, run the following script::

    .\appveyor\install_crlibm.bat

Finally, you can compile and install PyInterval::

    %PYTHON%\python setup.py install

.. _pypi: http://pypi.python.org/pypi/pyinterval/

Semantic Versioning
-------------------

Starting with version 1.0.0, this project follows a `semantic
versioning <http://semver.org/>`_ scheme.
