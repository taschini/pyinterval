# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

"""Mathematical function library for intervals.

This module provides transcendental functions with interval argument.
"""

try:
    import crlibm
except ImportError:
    import sys
    sys.stderr.write("Cannot load crlibm extension. The imath functions will not be available.\n")
    del sys
else:

    from . import interval, fpu

    class monotonic(object):
        def __init__(self, domain=None, rd=None, ru=None):
            self.domain = domain or interval[-fpu.infinity, fpu.infinity]
            self.rd = rd
            self.ru = ru

        def __call__(self, f):
            from functools import wraps
            self.rd = self.rd or getattr(crlibm, f.__name__ + '_rd')
            self.ru = self.ru or getattr(crlibm, f.__name__ + '_ru')
            @wraps(f)
            def wrapper(x):
                return interval._canonical(type(c)(self.rd(c.inf), self.ru(c.sup))
                                           for c in interval.cast(x) & self.domain)
            return wrapper

    @monotonic()
    def exp(x):
        "Exponential."

    @monotonic()
    def expm1(x):
        "exp(x) - 1."

    @monotonic(domain = interval[0, fpu.infinity])
    def log(x):
        "Natural logarithm."

    @monotonic(domain = interval[0, fpu.infinity])
    def log2(x):
        "Logarithm in base 2."

    @monotonic(domain = interval[0, fpu.infinity])
    def log10(x):
        "Logarithm in base 10."

    @monotonic(domain = interval[-1, fpu.infinity])
    def log1p(x):
        "log(1+x)."

    @monotonic()
    def atan(x):
        "Arc tangent."

    @monotonic()
    def atanpi(x):
        "atan(x)/pi."

    @monotonic()
    def sinh(x):
        "Hyberbolic sine."

    @interval.function
    def cosh(c):
        "Hyberbolic cosine."
        if c.inf > 0:
            return (crlibm.cosh_rd(c.inf), crlibm.cosh_ru(c.sup)),
        if c.sup < 0:
            return (crlibm.cosh_rd(c.sup), crlibm.cosh_ru(c.inf)),
        else:
            return (1.0, fpu.max(crlibm.cosh_ru(x) for x in c)),

    pi = 4 * atan(1)
    e = exp(1)

    def sqrt(x):
        "Square root."
        return interval.union(
            interval.hull(exp(log(e)/2).newton(lambda z: z**2 - e, lambda z: 2 * z) for e in c.extrema.components)
            for c in (x & interval[0, fpu.infinity]).components)

    def tanh():
        one_rd = crlibm.log_rd(crlibm.exp_rd(1))

        def tanh_rd(x):
            if x < 0:
                return -tanh_ru(-x)
            if x == fpu.infinity:
                return 1.0
            s, c = crlibm.sinh_rd(x), crlibm.cosh_ru(x)
            if fpu.infinity in (s, c):
                return one_rd
            return fpu.down(lambda: s/c)

        def tanh_ru(x):
            if x < 0:
                return -tanh_rd(-x)
            if x == fpu.infinity:
                return 1.0
            s, c = crlibm.sinh_ru(x), crlibm.cosh_rd(x)
            if fpu.infinity in (s, c):
                return 1.0
            return fpu.up(lambda: s/c)

        @monotonic(rd=tanh_rd, ru=tanh_ru)
        def tanh(c):
            "Hyberbolic tangent."

        return tanh
    tanh=tanh()

    @interval.function
    def cospi(c):
        "cos(pi*x)."
        d = fpu.up(lambda: c.sup - c.inf)
        if d != d or d >= 2.0:
            return (-1.0, +1.0),
        inf = fpu.min(crlibm.cospi_rd(x) for x in c)
        sup = fpu.max(crlibm.cospi_ru(x) for x in c)
        # The derivative of cospi is -pi*sinpi. As we are interested in the
        # derivative sign but not its magnitude, we omit the pi factor.
        if crlibm.sinpi_rd(c.inf) <= 0 <= crlibm.sinpi_ru(c.sup):
            return (inf, +1.0),
        if crlibm.sinpi_ru(c.inf) >= 0 >= crlibm.sinpi_rd(c.sup):
            return (-1.0, sup),
        if d >= 1.0:
            return (-1.0, +1.0),
        return (inf, sup),

    @interval.function
    def sinpi(c):
        "sin(pi*x)."
        d = fpu.up(lambda: c.sup - c.inf)
        if d != d or d >= 2.0:
            return (-1.0, +1.0),
        inf = fpu.min(crlibm.sinpi_rd(x) for x in c)
        sup = fpu.max(crlibm.sinpi_ru(x) for x in c)
        # The derivative of sinpi is pi*cospi. As we are interested in the
        # derivative sign but not its magnitude, we omit the pi factor.
        if crlibm.cospi_rd(c.inf) <= 0 <= crlibm.cospi_ru(c.sup):
            return (-1.0, sup),
        if crlibm.cospi_ru(c.inf) >= 0 >= crlibm.cospi_rd(c.sup):
            return (inf, +1.0),
        if d >= 1.0:
            return (-1.0, +1.0),
        return (inf, sup),

    @interval.function
    def tanpi(c):
        "tan(pi*x)."
        d = fpu.up(lambda: c.sup - c.inf)
        if d != d or d >= 1.0:
            return (-fpu.infinity, +fpu.infinity),
        if 0.0 in cospi(interval.new((c,))):
            def denan(x, ifnan):
                return x if x==x else ifnan
            return (denan(crlibm.tanpi_rd(c.inf), fpu.infinity), fpu.infinity), (-fpu.infinity, denan(crlibm.tanpi_ru(c.sup), -fpu.infinity))
        else:
            return (crlibm.tanpi_rd(c.inf), crlibm.tanpi_ru(c.sup)),

    @interval.function
    def cos(c):
        "Cosine."
        d = fpu.up(lambda: c.sup - c.inf)
        if d != d or d >= 2.0 * pi[0].inf:
            return (-1.0, +1.0),
        inf = fpu.min(crlibm.cos_rd(x) for x in c)
        sup = fpu.max(crlibm.cos_ru(x) for x in c)
        if crlibm.sin_rd(c.inf) <= 0 <= crlibm.sin_ru(c.sup):
            return (inf, +1.0),
        if crlibm.sin_ru(c.inf) >= 0 >= crlibm.sin_rd(c.sup):
            return (-1.0, sup),
        if d >= pi[0].inf:
            return (-1.0, +1.0),
        return (inf, sup),

    @interval.function
    def sin(c):
        "Sine."
        d = fpu.up(lambda: c.sup - c.inf)
        if d != d or d >= 2.0 * pi[0].inf:
            return (-1.0, +1.0),
        inf = fpu.min(crlibm.sin_rd(x) for x in c)
        sup = fpu.max(crlibm.sin_ru(x) for x in c)
        if crlibm.cos_rd(c.inf) <= 0 <= crlibm.cos_ru(c.sup):
            return (-1.0, sup),
        if crlibm.cos_ru(c.inf) >= 0 >= crlibm.cos_rd(c.sup):
            return (inf, +1.0),
        if d >= pi[0].inf:
            return (-1.0, +1.0),
        return (inf, sup),

    @interval.function
    def tan(c):
        "Tangent."
        d = fpu.up(lambda: c.sup - c.inf)
        if d != d or d >= pi[0].inf:
            return (-fpu.infinity, +fpu.infinity),
        if 0.0 in cos(interval.new((c,))):
            def denan(x, ifnan):
                return x if x==x else ifnan
            return (denan(crlibm.tan_rd(c.inf), fpu.infinity), fpu.infinity), (-fpu.infinity, denan(crlibm.tan_ru(c.sup), -fpu.infinity))
        else:
            return (crlibm.tan_rd(c.inf), crlibm.tan_ru(c.sup)),

    del monotonic

if __name__  == '__main__':
    import doctest
    doctest.testmod()
