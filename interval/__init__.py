# Copyright (c) 2008, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

"""An algebraically closed interval system on the extended real set.

This package provides the interval class, which is usually imported
into the current namespace:

    >>> from interval import interval
    >>> interval[1,2]
    interval([1.0, 2.0])

"""

from . import fpu
inf = fpu.infinity


def coercing(f):
    from functools import wraps
    @wraps(f)
    def wrapper(self, other):
        try:
            return f(self, self.cast(other))
        except self.ScalarError:
            return NotImplemented
    return wrapper


def comp_by_comp(f):
    from functools import wraps
    @wraps(f)
    def wrapper(self, other):
        try:
            return self._canonical(self.Component(*f(x, y)) for x in self for y in self.cast(other))
        except self.ScalarError:
            return NotImplemented
    return wrapper


class Metaclass(type):
    def __getitem__(self, arg):
        return self(arg)

    def reload(self):
        import sys, __main__
        module = reload(sys.modules[self.__module__])
        if __main__.interval == self:
            __main__.interval = module.interval

    def add_method(self, f):
        setattr(self, f.__name__, f)
        return f


class interval(tuple):
    """A (multi-)interval on the extended real set.

    An interval is an immutable object that is created by specifying
    the end-points of its connected components:

        >>> interval([0, 1], [2, 3], [10, 15])
        interval([0.0, 1.0], [2.0, 3.0], [10.0, 15.0])

    constructs an interval whose arbitrary element x must satisfy 0 <=
    x <= 1 or 2 <= x <= 3 or 10 <= x <= 15. Several shortcuts are
    available:

        >>> interval(1, [2, 3])
        interval([1.0], [2.0, 3.0])

        >>> interval[1, 2]
        interval([1.0, 2.0])

        >>> interval[1]
        interval([1.0])

    Intervals are closed with respect to all arithmetic operations,
    integer power, union, and intersection. Casting is provided for
    scalars in the real set.

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
        "Create a new interval from existing components."
        return tuple.__new__(cls, components)

    @classmethod
    def cast(cls, x):
        """Cast a scalar to an interval.

        If the argument is an interval, it is returned unchanged. If
        the argument is not a scalar an interval.ScalarError is
        raised::

            >>> interval.cast('asd')
            Traceback (most recent call last):
            ...
            ScalarError: Invalid scalar: 'asd'

        """
        if isinstance(x, cls):
            return x
        try:
            y = fpu.float(x)
        except:
            raise cls.ScalarError("Invalid scalar: " + repr(x))
        if isinstance(x, (int, long)) and x != y:
            # Special case for an integer with more bits than in a float's mantissa
            if x > y:
                return cls.new((cls.Component(y, fpu.up(lambda: y + 1)),))
            else:
                return cls.new((cls.Component(fpu.down(lambda: y - 1), y),))
        return cls.new((cls.Component(y, y),))

    @classmethod
    def function(cls, f):
        """Decorator creating an interval function from a function on a single component.

        The original function accepts one argument and returns a sequence
        of (inf, sup) pairs:

            >>> @interval.function
            ... def mirror(c):
            ...    return (-c.sup, -c.inf), c
            >>> mirror(interval([1, 2], 3))
            interval([-3.0], [-2.0, -1.0], [1.0, 2.0], [3.0])

        """

        from functools import wraps
        @wraps(f)
        def wrapper(x):
            return cls._canonical(cls.Component(*t) for c in cls.cast(x) for t in f(c))
        return wrapper

    @classmethod
    def _canonical(cls, components):
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
        return cls._canonical(c for i in intervals for c in i)

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
        return self._canonical(self.Component(x, x) for c in self for x in c)

    def __repr__(self):
        return self.format("%r")

    def __str__(self):
        return self.format("%s")

    def format(self, fs):
        """Format into a string using fs as format for the interval bounds.

        The argument fs can be any string format valid with floats:

            >>> interval[-2.1, 3.4].format("%+g")
            'interval([-2.1, +3.4])'

        """
        return type(self).__name__ + '(' + ', '.join('[' + ', '.join(fs % x for x in sorted(set(c))) + ']' for c in self) + ')'

    def __pos__(self):
        return self

    def __neg__(self):
        return self.new(self.Component(-x.sup, -x.inf) for x in self)

    @comp_by_comp
    def __add__(x, y):
        return (fpu.down(lambda: x.inf + y.inf), fpu.up(lambda: x.sup + y.sup))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    @comp_by_comp
    def __mul__(x, y):
        return (
            fpu.down(lambda: fpu.min((x.inf * y.inf, x.inf * y.sup, x.sup * y.inf, x.sup * y.sup))),
            fpu.up  (lambda: fpu.max((x.inf * y.inf, x.inf * y.sup, x.sup * y.inf, x.sup * y.sup))))

    def __rmul__(self, other):
        return self * other

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
        if n % 2:
            def pow(c):
                return (fpu.power_rd(c.inf, n), fpu.power_ru(c.sup, n))
        else:
            def pow(c):
                if c.inf > 0:
                    return (fpu.power_rd(c.inf, n), fpu.power_ru(c.sup, n))
                if c.sup < 0:
                    return (fpu.power_rd(c.sup, n), fpu.power_ru(c.inf, n))
                else:
                    return (0.0, fpu.max(fpu.power_ru(x, n) for x in c))
        return self._canonical(self.Component(*pow(c)) for c in self)

    @comp_by_comp
    def __and__(x, y):
        return (fpu.max((x.inf, y.inf)), fpu.min((x.sup, y.sup)))

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


    class ScalarError(ValueError):
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

        @property
        def inf_inv(self):
            return fpu.up(lambda: 1 / self.inf)

        @property
        def sup_inv(self):
            return fpu.down(lambda: 1 / self.sup)


    def newton(self, f, p, maxiter=10000, tracer_cb=None):
        """Find the roots of f(x) (where p=df/dx) within self using Newton-Raphson.

        For instance, the following solves x**3 == x in [-10, 10]:

            >>> interval[-10, 10].newton(lambda x: x - x**3, lambda x: 1 - 3*x**2)
            interval([-1.0], [0.0], [1.0])

            >>> interval[-1.5, 3].newton(lambda x: (x**2 - 1)*(x - 2), lambda x:3*x**2 - 4*x -1)
            interval([-1.0], [1.0], [2.0])

        """
        if tracer_cb is None:
            def tracer_cb(tag, interval): pass
        def step(x, i):
            return (x - f(x) / p(i)) & i
        def some(i):
            yield i.midpoint
            for x in i.extrema.components:
                yield x
        def branch(current):
            tracer_cb('branch', current)
            for n in xrange(maxiter):
                previous = current
                for anchor in some(current):
                    current = step(anchor, current)
                    if current != previous:
                        tracer_cb('step', current)
                        break
                else:
                    return current
                if not current:
                    return current
                if len(current) > 1:
                    return self.union(branch(c) for c in current.components)
            tracer_cb("abandon", current)
            return self.new(())
        return self.union(branch(c) for c in self.components)


def setup():
    # The decorator interval.function can only be used from outside
    # the original class scope.

    @interval.add_method
    @interval.function
    def inverse(c):
        """Return self ** -1, or, equivalently, 1 / self."""
        if c.inf <= 0 <= c.sup:
            return ((-fpu.infinity, c.inf_inv if c.inf != 0 else -fpu.infinity),
                    (c.sup_inv if c.sup != 0 else +fpu.infinity, +fpu.infinity))
        else:
            return (c.sup_inv, c.inf_inv),
setup()

# Clean up the namespace
del coercing, comp_by_comp, setup, Metaclass

from . import imath
