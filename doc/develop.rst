Development
===========

Setup
-----

.. highlight:: console

1. Clone this repository::

      $ git clone git@github.com:taschini/pyinterval.git
      $ cd pyinterval

2. Create a new virtual or `conda <https://conda.io/>`_ environment and
   activate it. For instance::

      $ virtualenv --no-site-packages env
      $ source env/bin/activate

   On Windows the activation script is in a different directory:

   .. code-block:: doscon

      ...> env\Scripts\activate

3. Use Pip to install all the dependencies::

      $ pip install -e '.[develop]'

4. Using `Tox <http://tox.readthedocs.io>`_ for testing requires
   `PyEnv <https://github.com/pyenv/pyenv>`_.


Common tasks
------------

* Run the tests for all the supported Python versions::

      $ tox

  If Tox fails with a message like::

      ERROR:   x.y.z: InterpreterNotFound

  you need to install that version of Python::

      $ pyenv install x.y.z

* Run the tests with the Python of your environment::

      $ python setup.py test

  or::

      $ py.test

* Run the tests and collect coverage statistics::

      $ py.test --cov

* Build the documentation::

      $ make -C doc html


Continuous integration
----------------------

This project uses the following services:

* `Travis CI <https://travis-ci.org>`_ to run tests on Unix-based
  systems.

* `AppVeyor <https://www.appveyor.com>`_ to run tests on Windows.

* `Read the Docs <https://readthedocs.org>`_ to build and host the
  documentation.

Which of these system is activated on a given branch depends on the
branch name:

* The **doc** branch is tracked as the latest documentation by "Read
  the Docs", and is ignored by both Travis CI and AppVeyor.

* The **appveyor** branch is ignored by Travis CI.

* Any other branch is observed by both Travis CI and AppVeyor.
