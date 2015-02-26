============
maypy
============

Maybe(or Optional) object for Python.


Install
=======

::

    $ pip install git+git://github.com/wakhub/maypy.git@master


Example
=======

.. code:: python

    from maypy import maybe, not_none
    
    @maybe
    def read_file(path):
        try:
            with open(file) as f:
                return f.read()
        except:
            return None

    content_ = read_file("path/to/file.txt")
    print(content_.or_("Not found"))

    with content_ as content:  # Raises ValueError if content was None
        print(content)

    @not_none
    def seisitive_func(v):
        if v is 'invalid':
            return None
        return v

    sensitive_func('valid')  # Returns 'valid'
    sensitive_func('invalid')  # Raises ValueError

    maybex = Maybe(2)
    maybey = Maybe(3)
    maybez = Maybe(None)
    print(maybex + maybey)  # 5?
    print(maybex - maybey)  # -1?
    print(maybex + maybez)  # <Nothing>
    print((maybex + maybez).or_(100))  # 100


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

