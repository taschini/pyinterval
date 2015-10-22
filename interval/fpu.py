# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

"""\
``interval.fpu`` --- FPU control and helper functions
-----------------------------------------------------

This module provides:

  1. Mechanisms for the control of the rounding modes of the
     floating-point unit (FPU);

  2. Helper functions that respect IEEE 754 semantics.

Limitations
    The current implementation of the FPU's rounding-mode control is
    thought to be not thread-safe.

"""

from __builtin__ import float


def _init_libm():
    "Initialize low-level FPU control using C99 primitives in libm."
    global _fe_upward, _fe_downward, _fegetround, _fesetround

    import platform
    processor = platform.processor()
    if processor == 'powerpc':
        _fe_upward, _fe_downward = 2, 3
    elif processor == 'sparc':
        _fe_upward, _fe_downward = 0x80000000, 0xC0000000
    else:
        _fe_upward, _fe_downward = 0x0800, 0x0400

    from ctypes import cdll
    from ctypes.util import find_library
    libm = cdll.LoadLibrary(find_library('m'))
    _fegetround, _fesetround = libm.fegetround, libm.fesetround


def _init_msvc():
    "Initialize low-level FPU control using the Microsoft VC runtime."
    global _fe_upward, _fe_downward, setup, _fegetround, _fesetround

    from ctypes import cdll
    global _controlfp
    _controlfp = cdll.msvcrt._controlfp
    _fe_upward, _fe_downward = 0x0200, 0x0100
    def _fegetround():
        return _controlfp(0, 0)
    def _fesetround(flag):
        _controlfp(flag, 0x300)


for _f in _init_libm, _init_msvc:
    try:
        _f()
        break
    except:
        pass
else:
    import warnings
    warnings.warn("Cannot determine FPU control primitives. The fpu module is not correcly initialized.", stacklevel=2)
try:
    del _f
except:
    pass


def infinity():
    global infinity, nan
    try:
        infinity = float('inf')
    except:
        import struct
        infinity = struct.unpack('!d','\x7f\xf0\x00\x00\x00\x00\x00\x00')[0]
    nan = infinity / infinity
infinity()


def isnan(x):
    "Return True if x is nan."
    return x != x


def down(f):
    "Perform a computation with the FPU rounding downwards."
    saved = _fegetround()
    try:
        _fesetround(_fe_downward)
        return f()
    finally:
        _fesetround(saved)


def up(f):
    "Perform a computation with the FPU rounding upwards."
    saved = _fegetround()
    try:
        _fesetround(_fe_upward)
        return f()
    finally:
        _fesetround(saved)


class NanException(ValueError):
    "Exception thrown when an unwanted nan is encountered."
    pass


def ensure_nonan(x):
    "Return x, throwing a NanException if x is nan."
    if isnan(x):
        raise NanException
    return x


def min(l):
    "Return the minimum of the elements in l, or nan if any element is nan."
    import __builtin__
    try:
        return __builtin__.min(ensure_nonan(x) for x in l)
    except NanException:
        return nan


def max(l):
    "Return the maximum of the elements in l, or nan if any element is nan."
    import __builtin__
    try:
        return __builtin__.max(ensure_nonan(x) for x in l)
    except NanException:
        return nan


def power_rn(x, n):
    "Raise x to the n-th power (with n positive integer), rounded to nearest."
    assert isinstance(n, (int, long)) and n >= 0
    l=();
    while n > 0:
        n, y= divmod(n, 2)
        l=(y, l)
    result = 1.0
    while l:
        y, l = l
        if y:
            result = result * result * x
        else:
            result = result * result
    return result


def power_ru(x, n):
    "Raise x to the n-th power (with n positive integer), rounded toward +inf."
    if x >= 0:
        return up(lambda: power_rn(x, n))
    elif n % 2:
        return - down(lambda: power_rn(-x, n))
    else:
        return up(lambda: power_rn(-x, n))


def power_rd(x, n):
    "Raise x to the n-th power (with n positive integer), rounded toward -inf."
    if x >= 0:
        return down(lambda: power_rn(x, n))
    elif n % 2:
        return - up(lambda: power_rn(-x, n))
    else:
        return down(lambda: power_rn(-x, n))
