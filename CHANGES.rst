History
-------

1.1.1 (2016-08-10)
^^^^^^^^^^^^^^^^^^

- Fixed `#5`_: Intervals can now be pickled and copied using the functions in the
  ``copy`` module.

.. _#5: https://github.com/taschini/pyinterval/issues/5


1.1.0 (2016-06-10)
^^^^^^^^^^^^^^^^^^

- Added support for Python 3.
- Added ``interval.fpu.isinteger`` as a portable way to check whether a
  value is an instance of an integer type.
- Spun off Python binding to CRlibm into a separate project: PyCRlibm_.

.. _PyCRlibm: https://github.com/taschini/pycrlibm


1.0.0 (2015-10-23)
^^^^^^^^^^^^^^^^^^

- Project hosting migrated from Google Code to GitHub.
- Using Travis CI and AppVeyor as continuous integration services.
- Added support for Python 2.6 and 2.7.
- Dropped support for Python 2.5.


1.0.b21 (2008-08-27)
^^^^^^^^^^^^^^^^^^^^

- Initial release.
