API Documentation
=================

This document details the API exposed by the modules that make up this library.

.. contents::

.. automodule:: interval
   :members:

   .. data:: inf

      Infinity in the sense of IEEE 754. Identical to :data:`interval.fpu.infinity`.

      >>> from interval import inf
      >>> inf + inf == inf
      True


.. automodule:: interval.fpu
   :members:

      Infinity in the sense of IEEE 754. Also exported  as :data:`interval.inf`.

      >>> from interval import fpu
      >>> fpu.infinity + fpu.infinity == fpu.infinity
      True

   .. data:: nan

      An instance of *not-a-number*, in the sense of IEEE 754. Note
      that you must not use `nan` in comparisons. Use `isnan`
      instead.

      >>> from interval import fpu
      >>> fpu.nan == fpu.nan
      False

      >>> fpu.isnan(fpu.nan)
      True


.. automodule:: interval.imath
   :members:
