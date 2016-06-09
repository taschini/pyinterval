Using intervals
===============

This document gives an overview of how to use the `interval` class.

.. contents::

Construction
------------

The ``interval`` package can be loaded into the Python interpreter with the statement ::

    >>> from interval import interval, inf, imath

which injects in the current namespace the interval class, a constant
representing the mathematical infinity, and a module providing
interval transcendental functions.

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

    >>> print((interval[1]/interval[3]).format('%.17f'))
    interval([0.33333333333333331, 0.33333333333333337])

inersected::

    >>> interval[1, 4] & interval[2, 5]
    interval([2.0, 4.0])

merged by set-theoretic union::

    >>> interval[1, 4] | interval[2, 5]
    interval([1.0, 5.0])

    >>> interval[1, 2] | interval[4, 5]
    interval([1.0, 2.0], [4.0, 5.0])

raised to integer power::

    >>> interval[-3, 2] ** 2
    interval([0.0, 9.0])

Scalar numbers are automatically cast as intervals when used as
operands together with intervals::

    >>> 1/interval[3] == interval[1]/interval[3]
    True

The `imath <#module-interval.imath>`_ module provides transcendental
functions that accept interval arguments. For instance,

    >>> imath.exp(interval[0, 1])
    interval([1.0, 2.7182818284590455])

Inspection
----------

The ``in`` operator can be used to test whether a scalar is contained
in an interval::

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

It is possible to iterate on the connected components of an interval
as in the statement ::

   >>> [x for x in interval([1, 2], 3).components]
   [interval([1.0, 2.0]), interval([3.0])]

The endpoints are given by ::

   >>> interval([1, 2], 3).extrema
   interval([1.0], [2.0], [3.0])

and the midpoints by ::

   >>> interval([1, 2], 3).midpoint
   interval([1.5], [3.0])
