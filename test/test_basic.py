# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

import unittest
from interval import interval, fpu


class FpuTestCase(unittest.TestCase):

    def test_third(self):
        "Nearest rounding of 1/3 is downwards."
        self.assertEqual(1/3.0, fpu.down(lambda: 1.0 / 3.0))
        self.assertTrue(1/3.0 < fpu.up(lambda: 1.0 / 3.0))
        self.assertEqual(-1/3.0, fpu.up(lambda: 1.0 / -3.0))
        self.assertTrue(-1/3.0 > fpu.down(lambda: 1.0 / -3.0))

    def test_fourth(self):
        " 1/4 is exact."
        self.assertEqual(1/4.0, fpu.down(lambda: 1.0 / 4.0))
        self.assertEqual(1/4.0, fpu.up(lambda: 1.0 / 4.0))
        self.assertEqual(-1/4.0, fpu.up(lambda: 1.0 / -4.0))
        self.assertEqual(-1/4.0, fpu.down(lambda: 1.0 / -4.0))

    def test_fifth(self):
        "Nearest rounding of 1/5 is upwards."
        self.assertEqual(1/5.0, fpu.up(lambda: 1.0 / 5.0))
        self.assertTrue(1/5.0 > fpu.down(lambda: 1.0 / 5.0))
        self.assertEqual(-1/5.0, fpu.down(lambda: 1.0 / -5.0))
        self.assertTrue(-1/5.0 < fpu.up(lambda: 1.0 / -5.0))

    def test_ieee754(self):
        "fpu.float respect ieee754 semantics."
        self.assertEqual(fpu.infinity + fpu.infinity, fpu.infinity)
        self.assertTrue(fpu.isnan(fpu.nan))
        self.assertTrue(fpu.isnan(0.0 * fpu.infinity))
        self.assertTrue(fpu.isnan(fpu.infinity - fpu.infinity))

    def test_float_coercion(self):
        "Only real-number scalars should be able to coerce as fpu.float"
        self.assertRaises(Exception, lambda: float(1,2))
        self.assertRaises(Exception, lambda: float((1,2)))
        self.assertRaises(Exception, lambda: float([1,2]))
        self.assertRaises(Exception, lambda: float('a'))
        self.assertRaises(Exception, lambda: float(1+1j))

    def test_min(self):
        "Verify corner cases with nan, -inf, +inf"
        self.assertEqual(fpu.min((1.0, 2.0)), 1.0)
        self.assertEqual(fpu.min((1.0, fpu.infinity)), 1.0)
        self.assertEqual(fpu.min((1.0, -fpu.infinity)), -fpu.infinity)
        self.assertTrue(fpu.isnan(fpu.min((1.0, -fpu.nan))))

    def test_max(self):
        "Verify corner cases with nan, -inf, +inf"
        self.assertEqual(fpu.max((1.0, 2.0)), 2.0)
        self.assertEqual(fpu.max((1.0, fpu.infinity)), fpu.infinity)
        self.assertEqual(fpu.max((1.0, -fpu.infinity)), 1.0)
        self.assertTrue(fpu.isnan(fpu.max((1.0, fpu.nan))))

    def test_power(self):
        x = 1/3.0
        # The cube of one third should depend on the rounding mode
        self.assertTrue(fpu.down(lambda: x*x*x) < fpu.up(lambda: x*x*x))
        # But using the built-in power operator, it doesn't necessarily do it
        # print fpu.down(lambda: x**3) < fpu.up(lambda: x**3))
        # So we define an integer power methods that does
        self.assertTrue(fpu.power_rd(x, 3) < fpu.power_ru(x, 3))
        self.assertTrue(fpu.power_rd(-x, 3) < fpu.power_ru(-x, 3))
        self.assertTrue(fpu.power_rd(x, 4) < fpu.power_ru(x, 4))
        self.assertTrue(fpu.power_rd(-x, 4) < fpu.power_ru(-x, 4))

        self.assertEqual(
            (fpu.down(lambda: x*x*x), fpu.up(lambda: x*x*x)),
            (fpu.power_rd(x, 3), fpu.power_ru(x, 3)))


class ModuleTestCase(unittest.TestCase):

    def test_namespace(self):
        import interval
        self.assertEqual(
            dir(interval),
            ['__builtins__', '__doc__', '__file__', '__name__', '__path__', 'fpu', 'imath', 'inf', 'interval'])


class IntervalTestCase(unittest.TestCase):

    def test_trivial_constructor(self):
        self.assertEqual(interval[1], ((1, 1),))
        self.assertEqual(interval(1), ((1, 1),))
        self.assertEqual(interval[1, 2], ((1, 2),))
        self.assertEqual(interval(1, 2), ((1, 1), (2, 2)))
        self.assertEqual(interval([1, 2], [3, 4]), ((1, 2), (3, 4)))
        self.assertEqual(interval([1,2]), interval(interval([1, 2])))

    def test_nan_constructor(self):
        self.assertEqual(interval[2, fpu.nan], ((-fpu.infinity, fpu.infinity),))
        self.assertEqual(interval[2, fpu.nan], ((-fpu.infinity, fpu.infinity),))
        self.assertEqual(interval(2, fpu.nan, 9), ((-fpu.infinity, fpu.infinity),))

    def test_failing_constructor(self):
        self.assertRaises(interval.ComponentError, lambda: interval[1, [2, 3]])
        self.assertRaises(interval.ComponentError, lambda: interval[1, 2, 3])
        self.assertRaises(interval.ComponentError, lambda: interval(0, [1, 2, 3]))
        self.assertRaises(interval.ComponentError, lambda: interval(0, [1, [2, 3]]))
        self.assertRaises(interval.ComponentError, lambda: interval['a', 1])

    def test_canonical_constructor(self):
        self.assertEqual(interval([1, 3], [4, 6], [2, 5], 9), ((1, 6), (9, 9)))
        self.assertEqual(interval[2 ** (52 + 1) - 1], interval[9007199254740991.0])
        self.assertEqual(interval[2 ** (52 + 1) + 1], interval[4503599627370496 * 2.0, 4503599627370497 * 2.0])
        self.assertEqual(interval[-2 ** (52 + 1) + 1], interval[-9007199254740991.0])
        self.assertEqual(interval[-2 ** (52 + 1) - 1], interval[-4503599627370497 * 2.0, -4503599627370496 * 2.0])
        self.assertEqual(interval[2 ** (52 + 2) + 1], interval[4503599627370496 * 4.0, 4503599627370497 * 4.0])
        self.assertEqual(interval[2 ** (52 + 2) + 2], interval[4503599627370496 * 4.0, 4503599627370497 * 4.0])
        self.assertEqual(interval[2 ** (52 + 2) + 3], interval[4503599627370496 * 4.0, 4503599627370497 * 4.0])
        self.assertEqual(interval[-2 ** (52 + 2) - 1], interval[-4503599627370497 * 4.0, -4503599627370496 * 4.0])
        self.assertEqual(interval[-2 ** (52 + 2) - 2], interval[-4503599627370497 * 4.0, -4503599627370496 * 4.0])
        self.assertEqual(interval[-2 ** (52 + 2) - 3], interval[-4503599627370497 * 4.0, -4503599627370496 * 4.0])

    def test_unary(self):
        self.assertEqual(interval[1, 2], +interval[1, 2])
        self.assertEqual(interval[-2, -1], -interval[1, 2])

    def test_sum(self):
        self.assertEqual(interval[-fpu.infinity, +fpu.infinity], interval[-fpu.infinity] + interval[fpu.infinity])
        self.assertEqual(interval[4, 6], interval[1, 2] + interval[3, 4])
        self.assertEqual(interval[3, fpu.infinity], interval[1, fpu.infinity] + interval[2])
        self.assertEqual(interval[-fpu.infinity, +fpu.infinity], interval[-fpu.infinity, -1] + interval[2, +fpu.infinity])
        self.assertEqual(interval[-fpu.infinity, +fpu.infinity], interval[-fpu.infinity] + interval[8, +fpu.infinity])
        self.assertEqual(interval([1, 2], [10, fpu.infinity]) + interval([1,9],[-2,-1]),  interval([-1, 1], [2, fpu.infinity]))
        self.assertEqual(interval[1, 9] + interval([1, 2], [10, fpu.infinity]), interval[2, fpu.infinity])

    def test_sum_coercion(self):
        self.assertEqual(interval[1,2] + 2, interval[3, 4])
        self.assertRaises(TypeError, lambda: interval[1,2] + 1j)
        self.assertEqual(1 + interval[4, 5], interval[5, 6])
        self.assertRaises(TypeError, lambda: (1, 2) + interval[1,2])
        self.assertEqual(fpu.infinity + interval[4, 5], interval[fpu.infinity])

    def test_sub(self):
        self.assertEqual(interval[1, 2] - interval[3, 4], interval[-3.0, -1.0])
        self.assertEqual(interval[1, 2] - 0.5, interval[0.5, 1.5])
        self.assertEqual(1.5 - interval[1, 2], interval[-0.5, 0.5])

    def test_mul(self):
        self.assertEqual(interval[-fpu.infinity, +fpu.infinity], fpu.infinity * interval[0])
        self.assertEqual(interval[+fpu.infinity], interval[+fpu.infinity] * interval[3])
        self.assertEqual(interval[-8, +10], interval[1, 2] * interval[-4, 5])
        self.assertEqual(interval[3, 8], interval[1, 2] * interval[3, 4])
        self.assertEqual(interval[-fpu.infinity, +fpu.infinity], interval[0,1 ] * interval[2, +fpu.infinity])
        self.assertEqual(interval[2, fpu.infinity], interval[-fpu.infinity,-2] * interval[-fpu.infinity,-1])
        self.assertEqual(interval([1, 2], [3, 4]) * interval[0.5, 2], interval[0.5, 8])
        self.assertEqual(interval[1, 2] * 2, interval[2, 4])

    def test_inverse(self):
        self.assertEqual(interval[0.5, 1], interval[1, 2].inverse())
        self.assertEqual(interval[-1, -0.5],(-interval[1, 2]).inverse())
        self.assertEqual(interval([-fpu.infinity, -1], [0.5, +fpu.infinity]), interval[-1,2].inverse())
        self.assertEqual(interval(-fpu.infinity, [1, +fpu.infinity]), interval[0,1].inverse())
        self.assertEqual(interval([-fpu.infinity, -2.0], [0.0, fpu.infinity]),
                         interval([-0.5, 0.5], [0.2, fpu.infinity]).inverse())

    def test_division(self):
        self.assertEqual(interval[-fpu.infinity, fpu.infinity], interval[0,1] / interval[0,1])
        self.assertEqual(interval[0.5], interval[1] / 2)
        self.assertEqual(interval[0.5], 1 / interval[2])

    def test_power(self):
        self.assertRaises(TypeError, lambda: interval[1, 2] ** (1.3))
        self.assertEqual((-interval[1, 2]).inverse(), (-interval[1, 2]) ** -1)
        self.assertEqual(interval[0, 4], interval[-1, 2] ** 2)
        self.assertEqual(interval[-27, 8], interval[-3, 2] ** 3)
        self.assertEqual(interval[-1, 2], (interval[-1,2]**-1)**-1)
        self.assertEqual(interval([-0.38712442133802405]) ** 3, interval([-0.058016524353106828, -0.058016524353106808]))

        self.assertEqual(
            interval[fpu.down(lambda: (1/3.0)*(1/3.0)), fpu.up(lambda: (1/3.0)*(1/3.0))],
            (interval[1]/3.0) ** 2)

        self.assertEqual(
            interval[fpu.down(lambda: (1/3.0)*(1/3.0)*(1/3.0)), fpu.up(lambda: (1/3.0)*(1/3.0)*(1/3.0))],
            (interval[1]/3.0) ** 3)

    def test_format(self):
        for x in interval[1], interval[1,2], interval([1,2], [3,4]):
            self.assertEqual(x, eval(repr(x)))

    def test_intersection(self):
        self.assertEqual(interval[1, 2] & interval[0, 3], interval[1, 2])
        self.assertEqual(interval[1.1, 1.9] & interval[1.3, 2.5], interval[1.3, 1.9])
        self.assertEqual(interval[1.1, 1.9] & interval[0.3, 0.7], interval())
        self.assertEqual(interval([1, 3], [4, 5]) & interval[2], interval[2])
        self.assertEqual(interval([1, 3], [4, 5]) & interval(2,4.5), interval(2, 4.5))
        self.assertEqual(interval[1, 2] & 1.2, interval(1.2))
        self.assertEqual(2.1 & interval[1, 2], interval())

    def test_union(self):
        self.assertEqual(interval([1, 6], 9), interval([1, 3], [4, 6]) | interval([2, 5], 9))
        self.assertEqual(interval[1, 2] | 2.1, interval([1, 2], 2.1))
        self.assertEqual(2.1 | interval[1, 2], interval([1, 2], 2.1))

    def test_hull(self):
        self.assertEqual(interval([1, 9]), interval.hull((interval([1, 3], [4, 6]), interval([2, 5], 9))))

    def test_inclusion(self):
        def verify_in(x, y):
            self.assertTrue(x in y)
            self.assertEqual(x & y, interval(x))

        verify_in(1.5, interval[1, 2])
        verify_in(1, interval[1, 2])
        verify_in(2, interval[1, 2])
        verify_in(interval[1, 2], interval[1, 2])
        verify_in(interval[1.1, 2], interval[1, 2])
        verify_in(interval[1, 1.8], interval[1, 2])
        verify_in(interval([1.1, 2.2], [3.3, 4.4]), interval(-1, [0, 2.5], [3, 5], [7, 9]))

        def verify_out(x, y):
            self.assertFalse(x in y)
            self.assertNotEqual(x & y, x)

        verify_out(0, interval[1, 2])
        verify_out(4, interval[1, 2])
        verify_out(interval[1, 3], interval[2, 4])
        verify_out(interval(1, 3), interval(2, 4))

    def test_extrema(self):
        self.assertEqual(interval(1, [2, 3], 4).extrema, interval(1, 2, 3, 4))

    def test_midpoint(self):
        self.assertEqual(interval[0, 4].midpoint, interval[2])
        self.assertEqual(interval(-1, 1, 4), interval(-1, [0, 2], [3, 5]).midpoint)


class NewtonTestCase(unittest.TestCase):

    def test_opts(self):
        self.assertRaises(TypeError, lambda: interval(0,1).newton(None, None, nonexisting=True))

    def test_cubic(self):
        self.assertEqual(
            interval[-2, 2].newton(lambda x: x**3 - x, lambda x: 3*x**2-1),
            interval(-1, 0, 1))
        self.assertEqual(
            interval[-5, 5].newton(lambda x: x**3 + x - 10, lambda x: 3*x**2 + 1),
            interval[2])
        self.assertEqual(
            interval[-5, 5].newton(lambda x: x**3 + x - 15, lambda x: 3*x**2 + 1),
            interval[5249383869325653 * 2.0 ** -51, 5249383869325655 * 2.0 ** -51])
       # The sharpest result would be with 5249383869325654 * 2.0 ** -51 as sup.

    def test_sqrt2(self):
        import math
        f, p = lambda x: x**2 - 2, lambda x: 2 * x
        u, v = 6369051672525772 * 2.0 **-52, 6369051672525773 * 2.0 **-52
        self.assertEqual(v, math.sqrt(2))
        s = interval[u, v]
        self.assertEqual(s, interval[0.1, 5].newton(f, p))
        self.assertEqual(s, interval[0, 2].newton(f, p))
        self.assertEqual(s, interval[-1, 10].newton(f, p))
        self.assertEqual(interval(), interval[2, 5].newton(f, p))
        self.assertEqual(-s, interval[-5, 0].newton(f, p))
        self.assertEqual(-s|s, interval[-5, +5].newton(f, p))


if __name__ == '__main__':
    unittest.main()
