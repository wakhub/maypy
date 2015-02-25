"""
Optional type for Python

"""
from functools import wraps
import operator


class Optional(object):
    """ Optional object

    >>> opt1_ = Optional(123)
    >>> opt2_ = Optional(None)
    >>> opt3_ = Optional(['A', 'B', 'C'])
    >>> opt1_, opt2_, opt3_
    (<Optional 123>, <Optional None>, <Optional ['A', 'B', 'C']>)
    >>> opt1_.get(), opt2_.get(), opt3_.get()
    (123, None, ['A', 'B', 'C'])
    >>> opt1_.exists(), opt2_.exists(), opt3_.exists()
    (True, False, True)
    >>> opt1_.or_('ABC'), opt2_.or_('ABC')
    (123, 'ABC')
    >>> opt1_ == opt2_
    False
    >>> opt1_ == Optional(123)
    True
    >>> opt1_ == Optional('123')
    False
    >>> with opt1_ as opt1:
    ...     print(opt1)
    ...
    123
    >>> value = None
    >>> try:
    ...     with opt2_ as opt2:
    ...         value = 'ABC'
    ... except ValueError:
    ...     value = 'DEF'
    ...
    >>> value
    'DEF'
    >>> opt1_ + opt1_, opt1_ - 100, opt1_ * 3, opt1_ / 3
    (<Optional 246>, <Optional 23>, <Optional 369>, <Optional 41>)
    >>> Optional('a') + Optional('b')
    <Optional ab>
    >>> Optional('a') + Optional(None)
    <Optional None>
    >>> Optional('a') + Optional(None).or_('B')
    <Optional aB>

    :param object value:
    """

    def __init__(self, value):
        self.__value = value

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.__value)

    def __str__(self):
        return str(self.__value)

    def __operation(self, operator_, other):
        if not self.exists():
            return Optional(None)
        if type(other) != Optional:
            return Optional(operator_(self.get(), other))
        if not other.exists():
            return Optional(None)
        return Optional(operator_(self.get(), other.get()))

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
        if type(other) != Optional:
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


def optional(f):
    """ Decorator for wrapping return value by Optional

    >>> @optional
    ... def f(v):
    ...     return v * 2 if 10 <= v else None
    ...
    >>> f(3).exists()
    False
    >>> f(10).get()
    20
    >>> f(123) == Optional(123 * 2)
    True
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        return Optional(f(*args, **kwds))
    return wrapper


if __name__ == '__main__':
    import doctest
    doctest.testmod()
