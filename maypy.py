from functools import wraps
import operator
import re


__version__ = '0.0.1'


class Maybe(object):
    """ Maybe object

    >>> maybe1_ = Maybe(123)
    >>> maybe2_ = Maybe(None)
    >>> maybe3_ = Maybe(['A', 'B', 'C'])
    >>> maybe1_, maybe2_, maybe3_
    (123?, None?, ['A', 'B', 'C']?)
    >>> maybe1_.get(), maybe2_.get(), maybe3_.get()
    (123, None, ['A', 'B', 'C'])
    >>> maybe1_.exists(), maybe2_.exists(), maybe3_.exists()
    (True, False, True)
    >>> maybe1_.or_('ABC'), maybe2_.or_('ABC')
    (123, 'ABC')
    >>> maybe1_ == maybe2_
    False
    >>> maybe1_ == Maybe(123)
    True
    >>> maybe1_ == Maybe('123')
    False
    >>> with maybe1_ as maybe1:
    ...     print(maybe1)
    ...
    123
    >>> value = None
    >>> try:
    ...     with maybe2_ as maybe2:
    ...         value = 'ABC'
    ... except ValueError:
    ...     value = 'DEF'
    ...
    >>> value
    'DEF'
    >>> maybex = Maybe(2)
    >>> maybey = Maybe(3)
    >>> maybez = Maybe(None)
    >>> maybex + maybey
    5?
    >>> maybex - maybey
    -1?
    >>> maybex + maybez
    <Nothing>
    >>> (maybex + maybey + maybez).or_(100)
    100

    :param object value:
    """

    def __init__(self, value):
        if type(value) is Maybe:
            self.__value = value.get()
        else:
            self.__value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        value = self.__value
        if type(value) is str:
            value = "'{}'".format(re.escape(value))
        return '{}?'.format(value)

    def __operation(self, operator_, other):
        if not self.exists():
            return Nothing()
        if type(other) != Maybe:
            if other is None:
                return Nothing()
            return Maybe(operator_(self.get(), other))
        if not other.exists():
            return Nothing()
        return Maybe(operator_(self.get(), other.get()))

    def __add__(self, other):
        return self.__operation(operator.__add__, other)

    def __sub__(self, other):
        return self.__operation(operator.__sub__, other)

    def __div__(self, other):
        return self.__operation(operator.__div__, other)

    def __mul__(self, other):
        return self.__operation(operator.__mul__, other)

    def __enter__(self):
        if not self.exists():
            raise ValueError('value not exists')
        return self.__value

    def __exit__(self, type, value, tb):
        pass

    def __eq__(self, other):
        if type(other) != Maybe:
            return False
        return self.__value == other.__value

    def get(self):
        """ Returns the value

        :rtype: object
        :throws: ValueError
        """
        return self.__value

    def exists(self):
        """ Returns True if value exists

        :rtype: bool
        """
        return self.__value is not None

    def or_(self, replacement):
        """ Return the value if value exists else replacement

        :param object replacement:
        :rtype: any
        """
        return self.__value if self.exists() else replacement


class Nothing(Maybe):
    """ Shortcut for Maybe(None) """

    def __init__(self):
        super(Nothing, self).__init__(None)

    def __repr__(self):
        return '<{}>'.format(str(self))

    def __str__(self):
        return 'Nothing'


def maybe(f):
    """ Decorator for wrapping return value by Maybe

    >>> @maybe
    ... def f(v):
    ...     return v * 2 if 10 <= v else None
    ...
    >>> f(3)
    <Nothing>
    >>> f(10)
    20?
    >>> f(123) == Maybe(123 * 2)
    True
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        ret = f(*args, **kwds)
        return Nothing() if ret is None else Maybe(ret)
    return wrapper


def not_none(f):
    """ Decorator for rejecting None as return

    >>> @not_none
    ... def f(v):
    ...     if v is 'invalid':
    ...         return None
    ...     return 'valid'
    ...
    >>> f('foo')
    'valid'
    >>> f('invalid')
    Traceback (most recent call last):
    ...
    ValueError: Return value has not to be None for @not_none
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        ret = f(*args, **kwds)
        if ret is None:
            raise ValueError('Return value has not to be None for @not_none')
        return ret
    return wrapper


if __name__ == '__main__':
    import doctest
    doctest.testmod()
