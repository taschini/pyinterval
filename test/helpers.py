# Copyright (c) 2008-2016, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

"""Helper functions for the testing of intervals and fpu.

This module provides helper functions that were deemed not fundamental
and were not included in the interval or the fpu modules.
"""

import sys

# We inject the interval class into the module namespace only for use in the
# doctests:
from interval import interval, fpu   # noqa


def ulprepr(x, bits=sys.float_info.mant_dig, mink=sys.float_info.min_exp - sys.float_info.mant_dig):
    "Return two integers n and k such that x = n * ulp(x), ulp(x) = 2 ** k."

    if x == 0:
        return 0, mink
    import math
    m, e = math.frexp(x)
    k = max((e - bits, mink))
    return int(m * 2 ** (e - k)), k


def nudge(x, dir):
    "Nudge a float in the specified direction as many steps as abs(dir)."
    if dir == 0:
        return x
    if dir > +1:
        return nudge(nudge(x, 1), dir - 1)
    if dir < -1:
        return nudge(nudge(x, -1), dir + 1)
    f = dir * 2 ** ulprepr(x)[1]
    y = x + f / 2.0
    if y != x:
        return y
    else:
        return x + f


def isexact(x):
    """True if all components of x contain exactly one number.

    For instance,

        >>> isexact(interval(1, 2))
        True
        >>> isexact(interval([1], [2, 3]))
        False

    """
    return all(c.inf == c.sup for c in x)


def ulpwidth(x):
    """The widths of the components of x expressed as ULPs."""
    def diff(a, b):
        if a == b:
            return 0
        if fpu.infinity in (a, b):
            return fpu.infinity
        x, e = ulprepr(a)
        y, f = ulprepr(b)
        h = min(e, f)
        return y * 2 ** (f - h) - x * 2 ** (e - h)
    return [diff(c.inf, c.sup) for c in x]


def issharp(x):
    """True if each component of x width is at most 1 ULP.

    For instance,

        >>> issharp(1/interval[3] | interval[2])
        True

    """
    return not x or max(ulpwidth(x)) <= 1
