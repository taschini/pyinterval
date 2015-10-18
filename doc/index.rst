Interval Arithmetic in Python
=============================

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
installed on your system. It is also possible to check-out the sources
from the subversion repository::

    svn checkout http://pyinterval.googlecode.com/svn/trunk/ pyinterval

.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pypi: http://pypi.python.org/pypi/pyinterval/
.. _crlibm: http://lipforge.ens-lyon.fr/www/crlibm/

Using intervals
---------------

The ``interval`` package can be loaded into the Python interpreter with the statement ::

    >>> from interval import interval, inf, imath

which injects in the current namespace the interval class, a constant
representing the mathematical infinity, and a module providing
interval transcendetal functions.

Intervals are immutable objects that can be created by specifying their connected components::

    >>> k = interval([0, 1], [2, 3], [10, 15])

creates an object representing the union of the mathematical intervals
[0, 1], [2, 3] and [10, 15].

    >>> interval[1, 2]
    interval([1.0, 2.0])

represents the mathematical interval [1, 2], not be confused with the
union of the one-point intervals {1} and {2}::

    >>> interval(1, 2)
    interval([1.0], [2.0])

An interval consisting of only one number can be instantiated with
either forms:

    >>> interval(1), interval[1]
    (interval([1.0]), interval([1.0]))

An empty interval has no components:

    >>> interval()
    interval()

Operations
----------

Intervals can be added::

    >>> interval[1, 2] + interval[4, 5]
    interval([5.0, 7.0])

subtracted::

    >>> interval[5, 7] - interval[1, 2]
    interval([3.0, 6.0])

multiplied::

    >>> interval[0, 2] * interval[4, inf]
    interval([-inf, inf])

divided::

    >>> print (interval[1]/interval[3]).format('%.17f')
    interval([0.33333333333333331, 0.33333333333333337])

inersected::

    >>> interval[1, 4] & interval[2, 5]
    interval([2.0, 4.0])

unioned::

    >>> interval[1, 4] | interval[2, 5]
    interval([1.0, 5.0])

    >>> interval[1, 2] | interval[4, 5]
    interval([1.0, 2.0], [4.0, 5.0])

raised to integer power::

    >>> interval[-3, 2] ** 2
    interval([0.0, 9.0])

Scalar numbers are automatically cast as interval when used as
operands together with intervals::

    >>> 1/interval[3] == interval[1]/interval[3]
    True

The `imath <#module-interval.imath>`_ module provides transcendental
functions that accept interval arguments. For instance,

    >>> imath.exp(interval[0, 1])
    interval([1.0, 2.7182818284590455])

Inspection
----------

The ``in`` operator can be used to test whether a scalar is in a interval::

    >>> 0 in interval[-1, 1]
    True

    >>> 0 in interval[1, 2]
    False

or whether an interval is a subset of another interval::

    >>> interval[1, 2] in interval[0, 3]
    True

    >>> interval[1, 2] in interval[1.5, 3]
    False


The ``len`` operator returns the number of connected components in the
interval::

    >>> len(interval())
    0

    >>> len(interval[1, 2])
    1

    >>> len(interval(1, 2))
    2

It is possible to iterate on an interval components as in the
statement ::

   >>> [x for x in interval([1, 2], 3).components]
   [interval([1.0, 2.0]), interval([3.0])]

The endpoints are given by ::

   >>> interval([1, 2], 3).extrema
   interval([1.0], [2.0], [3.0])

and the midpoints by ::

   >>> interval([1, 2], 3).midpoint
   interval([1.5], [3.0])


Modules
=================

The code is organized in three modules:

     * `interval <#module-interval>`_, providing the interval class;
     * `interval.fpu <#module-interval.fpu>`_, providing lower-level control and helper functions;
     * `interval.imath <#module-interval.imath>`_, imath, providing transendental functions for interval, akin to math for floats.

interval
--------

.. automodule:: interval
   :members:

   .. data:: inf

      Infinity in the sense of IEEE 754. Identical to :data:`interval.fpu.infinity`.

      >>> inf + inf == inf
      True


interval.fpu
------------

.. automodule:: interval.fpu
   :members:

   .. data:: infinity

      Infinity in the sense of IEEE 754. Also exported  as :data:`interval.inf`.

      >>> from interval import fpu
      >>> fpu.infinity + fpu.infinity == fpu.infinity
      True

   .. data:: nan

      An instance of not-a-number, also in the sense of IEEE 754. Note
      that you cannot use nan in conditional clauses. Use isnan
      instead.

      >>> from interval import fpu
      >>> fpu.nan == fpu.nan
      False

      >>> fpu.isnan(fpu.nan)
      True

interval.imath
--------------

.. automodule:: interval.imath
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
