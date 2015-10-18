===========================================================
Interval arithmetic: Python implementation and applications
===========================================================


Informal Introduction
=====================

The conventional use of interval arithmetic is to determine loss of
precision in floating-point operations. This topic, an important
topic, will be discussed in this paper too. What I find more exciting,
though, is the application of interval arithmetic to the solution of
equations, especially equations which might have more than one
solutions.

To do that, we have first to extend the conventional definition of
intervals. Normally a (closed) interval is a set containing all the
numbers between its bounds and including the bounds themselves. In
this paper, these intervals will be called *simple* intervals. With
*intervals* we'll denote instead a finite union of simple intervals,
i.e. a set of the form [a,b]U[c,d]U...U[y,z] conisting of the number
between a and b, between c and d, ... or between y and z.

This simple device allows us to build an interval system that is
closed under algebraical operations. An interval consisting of
disjoint components can then represent the multiple solutions to an
equation in the real domain. We'll see how a vanilla Newton-Raphson
implemented on intervals gives us this result for free.


Formal Introduction
===================

Following the work of Hansen and Walster [#HansenWalster]_, this paper
presents the Python implementation of an interval system in the extended
real set that is closed under arithmetic operations. Correct rounding
ensures that the operations are inclusion-wise monotonic.

Two main applications will be discussed:

(1) An interval-arithmetic Newton-Raphson algorithm for the solution
of equations in the real domain with possibly multiple solutions.

(2) Estimating the precision of numerical values produced by
floating-point computations.

Notation
========

..
    The interval library can be imported as
    >>> from interval import interval

In Python we'll write::

    >>> interval([0, 1], [2, 3], [10, 15])
    interval([0.0, 1.0], [2.0, 3.0], [10.0, 15.0])

to signify the union of the simple intervals [0, 1], [2, 3], [10, 15],
its *components*. There are shortcuts for important special cases. If
an interval consists of only one component it will be denoted as::

    >>> interval[1, 2]
    interval([1.0, 2.0])

and we'll write::

    >>> interval(1, 2)
    interval([1.0], [2.0])

for any component that degnerates to only one number.


Multiple solutions to an equation
=================================

The details of the interval-based Newton-Raphson require a bit more
mathematical typesetting capabilities than RST allows. At this stage I
can only show you a use case::

    >>> interval[-100, 100].newton(
    ...    f=lambda x: x**3 - x,
    ...    p=lambda x: 3*x**2 - 1)
    interval([-1.0], [-0.0], [1.0])

This code looks for the solutions to the equation ``x ** 3 == 1`` in
the interval [-100, 100] finding all the three of them.

Loss of precision in floating-point computations
================================================

The classic example is the function::

    >>> def f(x,y):
    ...    return (
    ...        (333.75-x**2)* y**6 + x**2 * (11* x**2 * y**2-121 * y**4 -2) +
    ...        5.5 * y**8 + x/(2*y))

which, evaluated at (77617, 33096) yields::

    >>> f(77617.0, 33096.0)
    1.1726039400531787

This result is wrong. Not a single digit is correct. You could use
gmpy [#gmpy]_, but you would still left wondering what precision you
would have to use::

    >>> import gmpy;                                      # doctest: +SKIP
    >>> f(gmpy.mpf(77617.0, 64), gmpy.mpf(33096.0, 64))   # doctest: +SKIP
    mpf('-4.29496729482739605995e9',64)
    >>> f(gmpy.mpf(77617.0, 65), gmpy.mpf(33096.0, 65))   # doctest: +SKIP
    mpf('-8.2739605994682136814116509548e-1',65)

One more bit causes 10 orders of magnitude of difference in the
outcome!  This means that **unless you know in advance** how many bits of
precision you need, **gmpy won't help you**.

Using intervals, instead, you always get an immediate indication of the
precision of the calculation::

    >>> print f(interval(77617.0), interval(33096.0)).format('%.17g')
    interval([-3.5417748621522339e+21, 3.5417748621522344e+21])

A spread of the twenty-one orders of magnitude in the result clearly
indicates that the loss of precision is total.

*NB: In this specific case, f is a ratio of two polynomials with
rational coefficients, so you can use gmpy.mpq to calculate the exact
value of f (once 333.75 and 5.5 have also been rewritten as rationals).*

Decimal
-------

Using the decimal library is no help in these circumstances:

    >>> from decimal import Decimal, getcontext
    >>> def fd(x,y):
    ...    return (
    ...        (Decimal('333.75')-x**2)* y**6 + x**2 * (11* x**2 * y**2-121 * y**4 -2) +
    ...        Decimal('5.5') * y**8 + x/(2*y))

With default precision you still get garbage

    >>> fd(Decimal(77617), Decimal(33096))
    Decimal('-999999998.8273960599468213681')

In order to get a decently approximated result you need to know in
advance the required precision

    >>> getcontext().prec = 37
    >>> fd(Decimal(77617), Decimal(33096))
    Decimal('-0.827396059946821368141165095479816292')


..
   clean up:

   >>> from decimal import setcontext, DefaultContext
   >>> setcontext(DefaultContext)

Implementation
==============

The implementation, which will be publicly released under the Python
Open Source lincese by the time of the conference, is entirely written
in Python. The rounding mode of the floating-point unit is controlled
by ``ctypes`` access to the standard C99 functions declared in fenv.h
[#fenv]_.

Optionally, CRlibm, the Correctly Rounded Mathematical Library
[#crlibm]_, can be used to provide transcendental functions over the
presented closed interval system.


Future directions
=================

An interesting further development of this work would be having the
intervals use multiple-precisions floating-point numbers in their
calculations, a sort of *intervals on gmpy*.


History
=======

I originally implemented a similar library in Ruby, which is still
available on-line [#ruby]_.  As my professional interests shifted
towards Python, I decided to reimplement the same fundamental ideas in
Python. Aside from the merits of the two languages, in the end what
mattered in my case was the community of people (and hence of
libraries and expertise) using Python for numerical applications.


References
==========

.. [#HansenWalster] Eldon Hansen, G. William Walster, Global Optimization Using Interval Analysis - Second Edition, Revised and Expanded. John Dekker, Inc., 2003.

.. [#gmpy] http://code.google.com/p/gmpy/

.. [#fenv] http://www.opengroup.org/onlinepubs/009695399/basedefs/fenv.h.html

.. [#crlibm] http://lipforge.ens-lyon.fr/www/crlibm/documentation.html

.. [#ruby] http://intervals.rubyforge.org/

..
   [#Goldberg] David Goldberg, What Every Computer Scientist Should Know About Floating-Point Arithmetic, ACM Computing Surveys, vol. 23 (1991), pp. 5--48.

..
   [#mpfr] http://www.mpfr.org/
