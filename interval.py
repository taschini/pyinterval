# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

"""An algebraically closed interval system on the extended real set.

This module provides the interval class, which is usually imported
into the current namespace:

    >>> from interval import interval
    >>> interval[1,2]
    interval([1.0, 2.0])

"""

import fpu


def coercing(f):
    from functools import wraps
    @wraps(f)
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            try:
                other = self.cast(other)
            except:
                return NotImplemented
        return f(self, other)
    return wrapper


class Metaclass(type):
    def __getitem__(self, arg):
        return self(arg)

    def reload(self):
        import sys
        module = sys.modules[self.__module__]
        main = sys.modules['__main__']
        reload(module)
        if main.interval == self:
            main.interval = module.interval


class interval(tuple):
    """A (multi-)interval on the extended real set.

    An interval is an immutable object.

        >>> interval([0, 1], [2, 3], [10, 15])
        interval([0.0, 1.0], [2.0, 3.0], [10.0, 15.0])

    constructs an interval with three components, but if the interval
    consists of only one component you can use the shorter form

        >>> interval[1, 2]
        interval([1.0, 2.0])

    Any component whose extrema coincide, a single number can be used
    to denote the whole component:

        >>> interval[1]
        interval([1.0])
        >>> interval[1] == interval(1)
        True

    Intervals are closed with respect to the arithmetic operations + -
    * /, integer power, and the set operations & |. Casting is
    provided for scalars in the real set.

        >>> (1 + interval[3, 4] / interval[-1, 2]) & interval[-5, 5]
        interval([-5.0, -2.0], [2.5, 5.0])

    """

    __metaclass__ = Metaclass

    def __new__(cls, *args):
        if len(args) == 1 and isinstance(args[0], cls):
            return args[0]
        def make_component(x, y=None):
            if y is None:
                return cls.cast(x)
            else:
                return cls.hull((cls.cast(x), cls.cast(y)))
        def process(x):
            try:
                return make_component(*x if hasattr(x, '__iter__') else (x,))
            except:
                raise cls.ComponentError("Invalid interval component: " + repr(x))
        return cls.union(process(x) for x in args)

    @classmethod
    def new(cls, components):
        return tuple.__new__(cls, components)

    @classmethod
    def cast(cls, x):
        y = float(x)
        if isinstance(x, (int, long)) and x != y:
            # Special case for an integer with more bits than in a float's mantissa
            if x > y:
                return cls.new((cls.Component(y, fpu.up(lambda: y + 1)),))
            else:
                return cls.new((cls.Component(fpu.down(lambda: y - 1), y),))
        return cls.new((cls.Component(y, y),))

    @classmethod
    def canonical(cls, components):
        from operator import itemgetter
        components = [c for c in components if c.inf <= c.sup]
        components.sort(key=itemgetter(0))
        l = []
        for c in components:
            if not l or c.inf > l[-1].sup:
                l.append(c)
            elif c.sup > l[-1].sup:
                l[-1] = cls.Component(l[-1].inf, c.sup)
        return cls.new(l)

    @classmethod
    def union(cls, intervals):
        """Return the union of the specified intervals.

        This class method is equivalent to the repeated use of the | operator.

            >>> interval.union([interval([1, 3], [4, 6]), interval([2, 5], 9)])
            interval([1.0, 6.0], [9.0])

            >>> interval([1, 3], [4, 6]) | interval([2, 5], 9)
            interval([1.0, 6.0], [9.0])

        """
        return cls.canonical(c for i in intervals for c in i)

    @classmethod
    def hull(cls, intervals):
        """Return the hull of the specified intervals.

        The hull of a set of intervals is the smallest connected
        interval enclosing all the intervals.

            >>> interval.hull((interval[1, 3], interval[10, 15]))
            interval([1.0, 15.0])

            >>> interval.hull([interval(1, 2)])
            interval([1.0, 2.0])

        """
        components = [c for i in intervals for c in i]
        return cls.new((cls.Component(fpu.min(c.inf for c in components), fpu.max(c.sup for c in components)),))

    @property
    def components(self):
        return (self.new((x,)) for x in self)

    @property
    def midpoint(self):
        return self.new(self.Component(x, x) for x in (sum(c)/2 for c in self))

    @property
    def extrema(self):
        return self.canonical(self.Component(x, x) for c in self for x in c)

    def __repr__(self):
        return self.format("%r")

    def __str__(self):
        return self.format("%s")

    def format(self, fs):
        """Format into a string using fs as format for the interval bounds.

            >>> interval[-2.1, 3.4].format("%+g")
            'interval([-2.1, +3.4])'

        """
        return type(self).__name__ + '(' + ', '.join('[' + ', '.join(fs % x for x in sorted(set(c))) + ']' for c in self) + ')'

    def __pos__(self):
        return self

    def __neg__(self):
        return self.new(self.Component(-x.sup, -x.inf) for x in self)

    @coercing
    def __add__(self, other):
        return self.canonical(
            self.Component(fpu.down(lambda: x.inf + y.inf), fpu.up(lambda: x.sup + y.sup))
            for x in self for y in other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    @coercing
    def __mul__(self, other):
        return self.canonical(
            self.Component(
                    fpu.down(lambda: fpu.min(x.cross(y))),
                    fpu.up  (lambda: fpu.max(x.cross(y))))
            for x in self for y in other)

    def __rmul__(self, other):
        return self * other

    def inverse(self):
        return self.canonical(x for c in self for x in c.inverse())

    @coercing
    def __div__(self, other):
        return self * other.inverse()

    __truediv__ = __div__

    @coercing
    def __rdiv__(self, other):
        return self.inverse() * other

    __rtruediv__ = __rdiv__

    def __pow__(self, n):
         if not isinstance(n, (int, long)):
             return NotImplemented
         if n < 0:
             return (self ** -n).inverse()
         return self.canonical(c ** n for c in self)

    @coercing
    def __and__(self, other):
        return self.canonical(
            self.Component(
                    fpu.max((x.inf, y.inf)),
                    fpu.min((x.sup, y.sup)))
            for x in self for y in other)

    def __rand__(self, other):
        return self & other

    @coercing
    def __or__(self, other):
        return self.union((self, other))

    def __ror__(self, other):
        return self | other

    @coercing
    def __contains__(self, other):
        return all(any(x.inf <= y.inf and y.sup <= x.sup for x in self) for y in other)


    class ComponentError(ValueError):
        pass


    class Component(tuple):

        def __new__(cls, inf, sup):
            if fpu.isnan(inf) or fpu.isnan(sup):
                return tuple.__new__(cls, (-fpu.infinity, +fpu.infinity))
            return tuple.__new__(cls, (inf, sup))

        @property
        def inf(self):
            return self[0]

        @property
        def sup(self):
            return self[1]

        def cross(self, other):
            return (self.inf * other.inf, self.inf * other.sup, self.sup * other.inf, self.sup * other.sup)

        @property
        def inf_inv(self):
            return fpu.up(lambda: 1 / self.inf)

        @property
        def sup_inv(self):
            return fpu.down(lambda: 1 / self.sup)

        def inverse(self):
            if self.inf <= 0 <= self.sup:
                return (
                    self.__class__(-fpu.infinity, self.inf_inv if self.inf != 0 else -fpu.infinity),
                    self.__class__(self.sup_inv if self.sup != 0 else +fpu.infinity, +fpu.infinity))
            else:
                return (self.__class__(self.sup_inv, self.inf_inv),)

        def __neg__(self):
            return self.__class__(-self.sup, -self.inf)

        def __pow__(self, n):
            if self.inf > 0:
                return self.__class__(
                    fpu.down(lambda: fpu.power(self.inf, n)),
                    fpu.up  (lambda: fpu.power(self.sup, n)))
            if self.sup < 0:
                if (-1) ** n > 0:
                    return (-self)**n
                else:
                    return - (-self)**n
            if (-1) ** n > 0:
                return self.__class__(
                    0,
                    fpu.max(fpu.up(lambda: (fpu.power(self.inf, n), fpu.power(self.sup, n)))))
            return self.__class__(
                fpu.down(lambda: fpu.power(self.inf, n)),
                fpu.up  (lambda: fpu.power(self.sup, n)))


    def newton(self, f, p, **opts):
        """Find the roots of f(x) (where p=df/dx) within self using Newton-Raphson.

        For instance, the following solves x**3 == x in [-10, 10]:

            >>> interval[-10, 10].newton(lambda x: x**3 - x, lambda x: 3*x**2 - 1)
            interval([-1.0], [-0.0], [1.0])

        """
        invalid = set(opts) - set(self.newton.options)
        if invalid:
            raise TypeError, "Unexpected keyword arguments: " + ', '.join(repr(x) for x in invalid)
        for k, v in self.newton.options.iteritems():
            opts.setdefault(k, v)
        def step(x, i):
            return (x - f(x) / p(i)) & i
        if opts['verbose']:
            def log(*a):
                print ' '.join(repr(x) for x in a)
        else:
            def log(*a):
                pass
        def branch(current):
            log("Branch", current)
            for n in xrange(opts['maxiter']):
                previous = current
                current = step(current.midpoint, current)
                log("Step", current)
                if previous == current:
                    splits = [c for c in (step(x, current) for x in self.extrema.components) if c and c != current]
                    log("Splits", *splits)
                    if splits:
                        return self.union(branch(c) for c in splits[:1])
                    return current
                if not current:
                    log("Dead end")
                    return current
                if len(current) > 1:
                    return self.union(branch(c) for c in current.components)
            log("Abandon")
            return self.new(())
        return self.union(branch(c) for c in self.components)

    newton.options = dict(maxiter = 10000, verbose = False)


# Clean up the namespace
del coercing, Metaclass


if __name__  == '__main__':
    import doctest
    doctest.testmod()
