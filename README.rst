============
optional.py
============

Optional type for Python


Example
=======

::

    from optional import optional
    
    @optional
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
- Python

  - `PyMonado
    <https://pypi.python.org/pypi/PyMonad/>`_
  - `either
    <https://pypi.python.org/pypi/either/0.2>`_

