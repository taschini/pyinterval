History
-------

1.2.1 (unreleased)
^^^^^^^^^^^^^^^^^^

- Test installation with an outdated Pip.


1.2.0 (2017-03-05)
^^^^^^^^^^^^^^^^^^

- To improve readability, do not test the examples in the
  documentation with Python 2.6.
- Code pathways that are specific to one Python version are marked
  with ``# pragma`` directives, and the collection of coverage
  statistics ignores them as appropriate.
- Add support for Python 3.6.
- Implement `#11`_: Take the absolute value of an interval.
- Provide a helpful message during installation if setuptools is
  outdated (`#13`_).

.. _#11: https://github.com/taschini/pyinterval/issues/11
.. _#13: https://github.com/taschini/pyinterval/issues/13

1.1.1 (2016-08-10)
^^^^^^^^^^^^^^^^^^

- Fix `#5`_: Intervals can now be pickled and used with the
  functions in the ``copy`` module.

.. _#5: https://github.com/taschini/pyinterval/issues/5


1.1.0 (2016-06-10)
^^^^^^^^^^^^^^^^^^

- Add support for Python 3.
- Add ``interval.fpu.isinteger`` as a portable way to check whether a
  value is an instance of an integer type.
- Spin off Python binding to CRlibm into a separate project: PyCRlibm_.

.. _PyCRlibm: https://github.com/taschini/pycrlibm


1.0.0 (2015-10-23)
^^^^^^^^^^^^^^^^^^

- Migrate Project hosting from Google Code to GitHub.
- Use Travis CI and AppVeyor as continuous integration services.
- Add support for Python 2.6 and 2.7.
- Drop support for Python 2.5.


1.0.b21 (2008-08-27)
^^^^^^^^^^^^^^^^^^^^

- Initial release.
