Import test
===========

* Verify that importing `interval` will provide a helpful message if `crlibm` is not installed::

  ```console
    $ cd $TESTDIR/..
    $ PYTHONPATH=. coverage run -p /dev/stdin <<EOF
    > import interval
    > EOF
    Cannot load crlibm extension. The imath functions will not be available.

  ```
