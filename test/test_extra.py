# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

import unittest, math, platform
from interval import fpu, interval, imath, inf
from test import helpers

class HelpersTestCase(unittest.TestCase):

    def test_init(self):
        # Alternative definition of infinity
        import struct
        infinity = struct.unpack('!d','\x7f\xf0\x00\x00\x00\x00\x00\x00')[0]
        self.assertEqual(fpu.infinity, infinity)

    def test_nudge(self):
        self.assertEqual(helpers.nudge(5249383869325653 * 2.0 ** -51, +1), 5249383869325654 * 2.0 ** -51)
        self.assertEqual(helpers.nudge(5249383869325653 * 2.0 ** -51, -1), 5249383869325652 * 2.0 ** -51)
        self.assertEqual(helpers.nudge(5249383869325652 * 2.0 ** -51, +2), 5249383869325654 * 2.0 ** -51)
        self.assertEqual(helpers.nudge(5249383869325654 * 2.0 ** -51, -2), 5249383869325652 * 2.0 ** -51)
        self.assertEqual(helpers.nudge(-5249383869325653 * 2.0 ** -51, +1), -5249383869325652 * 2.0 ** -51)
        self.assertEqual(helpers.nudge(-5249383869325653 * 2.0 ** -51, -1), -5249383869325654 * 2.0 ** -51)
        self.assertEqual(helpers.nudge(9007199254740991 * 2.0 ** -51, +1), 4503599627370496 * 2.0 ** -50)
        self.assertEqual(helpers.nudge(16.0, -1), 9007199254740991 * 2.0 ** -49)
        self.assertEqual(helpers.nudge(9007199254740991 * 2.0 ** -49, +1), 16.0)
        self.assertEqual(helpers.nudge(0, +1), 2.0 ** -1074)

    def test_ulprepr(self):
        self.assertEqual(helpers.ulprepr(5249383869325653 * 2.0 ** -51), (5249383869325653, -51))
        self.assertEqual(helpers.ulprepr(-5249383869325653 * 2.0 ** -51), (-5249383869325653, -51))
        self.assertEqual(helpers.ulprepr(1/3.0), (0x15555555555555, -54))
        self.assertEqual(helpers.ulprepr(1/5.0), (0x1999999999999a, -55))
        self.assertEqual(helpers.ulprepr(33 * 2.0 ** -(1023+51)), (33, -1074))
        self.assertEqual(helpers.ulprepr(0.0), (0, -1074))

    def test_width(self):
        self.assertEqual(helpers.ulpwidth(interval[3]**-1), [1])
        self.assertEqual(helpers.ulpwidth(interval([9007199254740991 * 2.0 ** -51, 4503599627370496 * 2.0 ** -50],
                                  [9007199254740991 * 2.0 ** -49, 16],
                                  [-16, -9007199254740991 * 2.0 ** -49],
                                  )),[1, 1, 1])
        self.assertEqual(helpers.ulpwidth(interval([5249383869325653 * 2.0 ** -51, 5249383869325655 * 2.0 ** -51])),[2])
        self.assertEqual(helpers.ulpwidth(interval[123.34]), [0])
        self.assertEqual(helpers.ulpwidth(interval[fpu.infinity]), [0])
        self.assertEqual(helpers.ulpwidth(interval[2, fpu.infinity]), [fpu.infinity])

    def test_predicates(self):
        self.assertTrue(helpers.isexact(interval[1.23]))
        self.assertTrue(helpers.issharp(interval[1.23]))
        self.assertFalse(helpers.isexact(1/interval[23]))
        self.assertTrue(helpers.issharp(1/interval[23]))
        self.assertFalse(helpers.isexact(interval[1, 2]))
        self.assertFalse(helpers.issharp(interval[1, 2]))
        self.assertTrue(helpers.isexact(interval[fpu.infinity]))


class ExtraNewtonTestCase(unittest.TestCase):

    def assertApproximate(self, value, reference, maxdelta):
        self.assertEqual(max(helpers.ulpwidth(value) or [0]), maxdelta)
        self.assertTrue(value == reference or reference in value)

    def test_dennis_schnabel(self):
        def f(x):
            return (((x - 12) * x + 47 ) * x - 60 )* x
        def p(x):
            return ((4 * x - 12*3) * x + 47*2) * x - 60
        self.assertApproximate(interval[-100, 100].newton(f, p), interval(0, 3, 4, 5), 43)
        self.assertApproximate(interval[-100, 100].newton(lambda x: f(x) + 24, p), interval(0.888305779071752, 1), 59)
        self.assertApproximate(interval[-100, 100].newton(lambda x: f(x) + 24.1, p), interval(), 0)

    def test_exp(self):
        z = interval[-100, 100].newton(lambda x: imath.exp(x) + x, lambda x: imath.exp(x) + 1)
        assert z == interval[-0.56714329040978395, helpers.nudge(-0.56714329040978395, +1)]

        w = interval[-100, 100].newton(lambda x: imath.exp(-x)*x + 1, lambda x: imath.exp(-x)*(1-x))
        assert z == w

    def test_trig(self):
        z = interval[-10, 10].newton(lambda x: imath.cospi(x/3) - 0.5, lambda x: -imath.pi * imath.sinpi(x/3) / 3)
        w = interval(-7, -5, -1, 1, 5, 7)
        assert w in z
        assert max(helpers.ulpwidth(z)) == 4

class ImathTestcase(unittest.TestCase):

    def test_exp(self):
        self.assertEqual(imath.exp(0), interval[1])
        self.assertEqual(imath.exp(1), interval[math.e, helpers.nudge(math.e, +1)])
        self.assertEqual(imath.exp(interval([-fpu.infinity, 0], [1, fpu.infinity])),
                         interval([0, 1], [math.e, fpu.infinity]))

    def test_expm1(self):
        self.assertEqual(imath.expm1(0), interval[0])
        assert imath.expm1(1) in (imath.exp(1) - 1)

    def test_log(self):
        self.assertEqual(imath.log(1), interval[0])
        self.assertEqual(imath.log(0), interval[-fpu.infinity])
        self.assertEqual(imath.log(imath.exp(1)), interval[helpers.nudge(1, -1), helpers.nudge(1, +1)])
        self.assertEqual(imath.log(0), interval[-fpu.infinity])
        self.assertEqual(imath.log(interval[0, 1]), interval[-fpu.infinity, 0])
        self.assertEqual(imath.log(interval[-1, 1]), interval[-fpu.infinity, 0])
        self.assertEqual(imath.log(interval[-2, -1]), interval())

    def test_log2(self):
        self.assertEqual(imath.log2(2), interval[1])
        self.assertEqual(imath.log2(interval[-3, 2]), interval[-fpu.infinity, 1])

    def test_log10(self):
        self.assertEqual(imath.log10(interval[-5, 10]), interval[-fpu.infinity, 1])
        # The following fails on Win at 32 bits
        if not (platform.system() == 'Windows' and platform.architecture()[0] == '32bit'):
            self.assertEqual(imath.log10(10), interval[1])

    def test_log1p(self):
        self.assertEqual(imath.log1p(0), interval[0])
        self.assertEqual(imath.log1p(-1), interval[-fpu.infinity])
        self.assertEqual(imath.log1p(interval[-2, 0]), interval[-fpu.infinity, 0])
        self.assertEqual(imath.log1p(1), imath.log(2))

    def test_atan(self):
        pi4p = helpers.nudge(math.pi / 2, +1)
        self.assertEqual(imath.atan(interval[-fpu.infinity, fpu.infinity]),
                         interval([-pi4p, pi4p]))
        self.assertEqual(imath.atan(1), interval[math.pi / 4, helpers.nudge(math.pi / 4, +1)])

    def test_atanpi(self):
        self.assertEqual(imath.atanpi(interval[-fpu.infinity, fpu.infinity]), interval[-0.5, 0.5])
        # The following fails on Win at 32 bits
        if not (platform.system() == 'Windows' and platform.architecture()[0] == '32bit'):
            self.assertEqual(imath.atanpi(1), interval[0.25, helpers.nudge(0.25, +1)])

    def test_sinh(self):
        self.assertEqual(imath.sinh(0), interval[0])
        assert imath.sinh(1) in ((imath.exp(1) - imath.exp(-1))/2)

    def test_cosh(self):
        self.assertEqual(imath.cosh(0), interval[1])
        assert imath.cosh(2) in (imath.exp(2) + imath.exp(-2))/2
        assert imath.cosh(interval[1, 2]) == interval.hull((imath.cosh(1), imath.cosh(2)))
        assert imath.cosh(interval[-2, -1])  == imath.cosh(interval[1, 2])
        assert imath.cosh(interval[-2, 1]) == interval.hull((interval[1], imath.cosh(2)))
        assert imath.cosh(interval[-1, 2]) == interval.hull((interval[1], imath.cosh(2)))

    def test_sqrt(self):
        f, p = lambda x: x**2 - 2, lambda x: 2 * x
        self.assertEqual(imath.sqrt(2), interval[1.4142135623730949, 1.4142135623730951])
        self.assertEqual(imath.sqrt(4), interval[2])
        self.assertEqual(imath.sqrt(interval[-3, -1]), interval())
        self.assertEqual(imath.sqrt(interval[-1, 4]), interval([0.0, 2]))
        self.assertEqual(imath.sqrt(interval([-3.14, 2], [4,9], [25, 64])), interval([0, 1.4142135623730951], [2, 3], [5, 8]))

    def test_tanh(self):
        tanh = imath.tanh
        inf = fpu.infinity
        assert tanh(0) == interval[0]
        assert tanh(inf) == interval[1.0]
        assert tanh(-inf) == interval[-1.0]
        assert tanh(-12347.1234) == interval[-1, helpers.nudge(-1.0,+1)]

        def check(x):
            x = interval(x)
            z = tanh(x)
            assert z in imath.sinh(x)/imath.cosh(x)

        check(1)
        check(-0.123)
        check(9.9873e20)
        check(-12347.1234)
        check(interval[1,2])
        check(interval[-5.1, 1.2])

        from random import seed, random
        seed(123456)
        for i in xrange(100):
            x = random()
            check(x)
            check(1/x)
            check(-x)
            check(-1/x)

    def test_cospi(self):
        assert imath.cospi(fpu.infinity) == interval[-1, 1]
        assert imath.cospi(-fpu.infinity) == interval[-1, 1]
        assert imath.cospi(interval[0.5, 1.5]) == interval[-1, 0]
        assert imath.cospi(interval[-0.5, 0.5]) == interval[0, 1]
        assert imath.cospi(1/interval[3]) == interval[helpers.nudge(0.5,-2), helpers.nudge(0.5, 1)]
        assert imath.cospi(-1/interval[3]) == interval[helpers.nudge(0.5,-2), helpers.nudge(0.5, 1)]
        assert imath.cospi(2/interval[3]) == interval[helpers.nudge(-0.5,-2), helpers.nudge(-0.5,2)]
        assert imath.cospi(interval[6]**-1) == imath.sqrt(3)/2

    def test_sinpi(self):
        assert imath.sinpi(fpu.infinity) == interval[-1, 1]
        assert imath.sinpi(-fpu.infinity) == interval[-1, 1]
        assert imath.sinpi(interval[0, 1]) == interval[0, 1]
        assert imath.sinpi(interval[-1, 0]) == interval[-1, 0]
        assert imath.sinpi(1/interval[6]) == interval[helpers.nudge(0.5,-1), helpers.nudge(0.5, 1)]
        assert imath.sinpi(1/interval[-6]) == interval[helpers.nudge(-0.5,-1), helpers.nudge(-0.5, 1)]

    def test_tanpi(self):
        assert imath.tanpi(fpu.infinity) == interval[-fpu.infinity, fpu.infinity]
        assert imath.tanpi(-fpu.infinity) == interval[-fpu.infinity, fpu.infinity]
        assert imath.tanpi(-1.25) == -interval[1]
        assert imath.tanpi(-0.75) ==  interval[1]
        assert imath.tanpi(-0.25) == -interval[1]
        assert imath.tanpi(0.25)  ==  interval[1]
        assert imath.tanpi(0.75)  == -interval[1]
        assert imath.tanpi(1.25)  ==  interval[1]
        assert imath.tanpi(0.5)   ==  interval(-inf, +inf)
        assert imath.tanpi(-0.5)  ==  interval(-inf, +inf)
        assert imath.tanpi(1.5)   ==  interval(-inf, +inf)
        assert imath.tanpi(-1.5)  ==  interval(-inf, +inf)
        assert imath.tanpi(interval[-0.25, 0.25]) == interval[-1, 1]
        assert imath.tanpi(interval[0.25, 0.75]) == interval([-inf, -1], [1, +inf])

    def test_trig(self):
        assert imath.sin(imath.pi/2) == interval[helpers.nudge(1, -1), 1]
        assert imath.cos(imath.pi) == interval[-1, helpers.nudge(-1, +1)]
        assert imath.cos(imath.pi/interval[3]) == interval[helpers.nudge(0.5,-6), helpers.nudge(0.5, 1)]
        assert imath.tan(imath.pi/4) == interval[helpers.nudge(1,-1), helpers.nudge(1, +1)]

    def test_constants(self):
        assert helpers.issharp(imath.pi)
        assert helpers.issharp(imath.e)
        assert imath.pi == interval[7074237752028440 * 2.0 ** -51, 7074237752028441 * 2.0 ** -51]
        assert imath.e == interval[6121026514868073 * 2.0 ** -51, 6121026514868074 * 2.0 ** -51]

def within(x, y, d):
    return y in x and all(c < d for c in helpers.ulpwidth(x))

if __name__ == '__main__':
    unittest.main()
