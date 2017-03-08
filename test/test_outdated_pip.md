Setup test
==========

* Verify that setup will provide a helpful message in case of an
  outdated Pip installation::

  ```console
    $ (cd $TESTDIR/..; python setup.py)
    
    To install this library your must upgrade pip.
    Please run:
       python -m pip install --upgrade pip
    
    [1]
  ```
