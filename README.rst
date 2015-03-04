============
maypy
============

Maybe(or Optional) object for Python which is inspired by `Guava <https://github.com/google/guava>`_


Install
=======

::

    $ pip install --upgrade -e git+git://github.com/wakhub/maypy.git@master


Example
=======

.. code:: python

    from maypy import maybe, not_none, Maybe
    
    @maybe
    def read_file(path):
        try:
            with open(file) as f:
                return f.read()
        except:
            return None

    content_ = read_file("path/to/file.txt")
    print(content_.get())  # Raises ValueError if content was None
    print(content_.or_("Not found"))

    @not_none
    def seisitive_func(v):
        if v is 'invalid':
            return None
        return v

    sensitive_func('valid')  # Returns 'valid'
    sensitive_func('invalid')  # Raises ValueError

    x_ = Maybe(2)
    y_ = Maybe(3)
    z_ = Maybe(None)
    print(x_ + y_)            # 5?
    print(x_ - y_)            # -1?
    print(x_ + z_)            # <Nothing>
    print(x_ + z_).or_(100))  # 100
    print(x_ + 100)           # 102?


Tests
======

::

    $ python -m doctest -v maypy.py


References
===========

- `Data.Maybe (hackage.haskell.org)
  <https://hackage.haskell.org/package/base/docs/Data-Maybe.html>`_
- `Optional (Java Platform SE 8 )
  <http://docs.oracle.com/javase/8/docs/api/java/util/Optional.html>`_
- `Optional (Guava: Google Core Libraries for Java 19.0-SNAPSHOT API)
  <http://docs.guava-libraries.googlecode.com/git/javadoc/com/google/common/base/Optional.html>`_
- `The Swift Programming Language: Optional Chaining
  <https://developer.apple.com/library/ios/documentation/Swift/Conceptual/Swift_Programming_Language/OptionalChaining.html>`_
- `[Python-Dev] Surely "nullable" is a reasonable name?
  <https://mail.python.org/pipermail/python-dev/2014-August/135650.html>`_
- Similar Python modules

  - `null <https://pypi.python.org/pypi/null>`_
  - `sentinels <https://pypi.python.org/pypi/sentinels>`_
  - `nulltype <https://pypi.python.org/pypi/nulltype>`_
  - `PyMonado <https://pypi.python.org/pypi/PyMonad/>`_
  - `either <https://pypi.python.org/pypi/either/0.2>`_

