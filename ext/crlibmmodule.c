/* Copyright (c) 2008, Stefano Taschini <taschini@ieee.org> */
/* All rights reserved.                                     */
/* See LICENSE for details.                                 */

#include <Python.h>

#include "crlibm.h"

#define IMPLEMENT_AS(libfun, method)                        \
static PyObject * method(PyObject *self, PyObject *args)    \
{                                                           \
  double x=0.0;                                             \
  if (!PyArg_ParseTuple(args, "d", &x)) return NULL;        \
  return Py_BuildValue("d", libfun(x));                     \
}

#define IMPLEMENT_ROUND(name, round)                        \
IMPLEMENT_AS(name ## round, crlibm_ ## name ## round)

#define IMPLEMENT(name)                                     \
IMPLEMENT_ROUND(name, _rn)                                  \
IMPLEMENT_ROUND(name, _ru)                                  \
IMPLEMENT_ROUND(name, _rd)                                  \
IMPLEMENT_ROUND(name, _rz)


#define DECLARE_AS(name, method, doc)                       \
{#name,  method, METH_VARARGS, doc},

#define DECLARE_ROUND(name, round, doc)                     \
DECLARE_AS(name ## round, crlibm_ ## name ## round, doc)

#define DECLARE(name, doc)                                  \
DECLARE_ROUND(name, _rn, doc " rounded to nearest.")        \
DECLARE_ROUND(name, _ru, doc " rounded toward +inf.")       \
DECLARE_ROUND(name, _rd, doc " rounded toward -inf.")       \
DECLARE_ROUND(name, _rz, doc " rounded toward zero.")


IMPLEMENT(exp)
IMPLEMENT(log)
IMPLEMENT(cos)
IMPLEMENT(sin)
IMPLEMENT(tan)
IMPLEMENT(cospi)
IMPLEMENT(sinpi)
IMPLEMENT(tanpi)
IMPLEMENT(atan)
IMPLEMENT(atanpi)
IMPLEMENT(cosh)
IMPLEMENT(sinh)
IMPLEMENT(log2)
IMPLEMENT(log10)
IMPLEMENT(asin)
IMPLEMENT(acos)
IMPLEMENT(asinpi)
IMPLEMENT(acospi)
IMPLEMENT(expm1)
IMPLEMENT(log1p)

static char _crlibm_docs[] =
"Efficient and proven correctly-rounded mathematical library.\n\n"

"CRlibm is a free mathematical library (libm) which provides:\n\n"

"    * implementations of the double-precision C99 standard elementary\n"
"      functions,\n\n"

"    * correctly rounded in the four IEEE-754 rounding modes,\n\n"

"    * with a comprehensive proof of both the algorithms used and their\n"
"      implementation,\n\n"

"    * sufficiently efficient in average time, worst-case time, and\n"
"      memory consumption to replace existing libms transparently,\n\n"

"CRlibm is distributed under the GNU Lesser General Public License (LGPL).\n\n"

"Site: http://lipforge.ens-lyon.fr/www/crlibm/\n\n"

"Authors: David Defour, Catherine Daramy, Florent de Dinechin,\n"
"Matthieu Gallet, Nicolas Gast, Christoph Lauter, Jean-Michel Muller.\n\n"

"Python bindings by Stefano Taschini, http://www.taschini.net/ .";

static PyMethodDef _crlibm_methods[] = {
  DECLARE(exp, "exp(x)")
  DECLARE(log, "log(x)")
  DECLARE(cos, "cos(x)")
  DECLARE(sin, "sin(x)")
  DECLARE(tan, "tan(x)")
  DECLARE(cospi, "cos(pi * x)")
  DECLARE(sinpi, "sin(pi * x)")
  DECLARE(tanpi, "tan(pi * x)")
  DECLARE(atan, "atan(x)")
  DECLARE(atanpi, "atan(x)/pi")
  DECLARE(cosh, "cosh(x)")
  DECLARE(sinh, "sinh(x)")
  DECLARE(log2, "log(x)/log(2)")
  DECLARE(log10, "log(x)/log(10)")
  DECLARE(asin, "asin(x)")
  DECLARE(acos, "acos(x)")
  DECLARE(asinpi, "asin(x)/pi")
  DECLARE(acospi, "acos(x)/pi")
  DECLARE(expm1, "exp(x)-1")
  DECLARE(log1p, "log(1+x)")
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initcrlibm(void)
{
  crlibm_init();
  (void) Py_InitModule3("crlibm", _crlibm_methods, _crlibm_docs);
}
