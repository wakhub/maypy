from functools import wraps
import operator
import re


__version__ = '0.0.3'


class Maybe(object):
    """ Maybe object

    >>> x_ = Maybe(123)
    >>> y_ = Maybe(None)
    >>> z_ = Maybe(['A', 'B', 'C'])
    >>> x_, y_, z_
    (123?, None?, ['A', 'B', 'C']?)
    >>> x_.get()
    123
    >>> y_.get()
    Traceback (most recent call last):
    ...
    ValueError
    >>> x_.exists(), y_.exists(), z_.exists()
    (True, False, True)
    >>> x_.or_('ABC'), y_.or_('ABC'), z_.or_('ABC')
    (123, 'ABC', ['A', 'B', 'C'])
    >>> x_ == y_
    False
    >>> x_ == Maybe(123)
    True
    >>> x_ == Maybe('123')
    False


    Operators

    >>> x_ = Maybe(2)
    >>> y_ = Maybe(3)
    >>> z_ = Maybe(None)
    >>> x_ + y_
    5?
    >>> x_ - y_
    -1?
    >>> x_ + y_ + z_
    <Nothing>
    >>> (x_ + y_ + z_).get()
    Traceback (most recent call last):
    ...
    ValueError
    >>> (x_ + y_ + z_).or_(100)
    100
    >>> x_ + 100
    102?
    >>> x_ + None
    <Nothing>

    :param object value:
    """

    def __init__(self, value):
        if isinstance(value, Maybe):
            self.__value = value.get()
        else:
            self.__value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        value = self.__value
        if isinstance(value, str):
            value = "'{}'".format(re.escape(value))
        return '{}?'.format(value)

    def __add__(self, other):
        return self.__operation(operator.__add__, other)

    def __sub__(self, other):
        return self.__operation(operator.__sub__, other)

    def __div__(self, other):
        return self.__operation(operator.__div__, other)

    def __mul__(self, other):
        return self.__operation(operator.__mul__, other)

    def __eq__(self, other):
        if isinstance(other, Maybe):
            return self.__value == other.__value
        return self.__value == other

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

    def get(self):
        """ Returns the value

        :rtype: any
        :throws: ValueError
        """
        if self.exists():
            return self.__value
        raise ValueError()

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
    """ Alias of Maybe(None) """

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
    """ Decorator for rejecting None as return value

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
    ValueError: Return value must not to be None for @not_none
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        ret = f(*args, **kwds)
        if ret is None:
            raise ValueError('Return value must not to be None for @not_none')
        return ret
    return wrapper


class MaybeDict(object):
    """ The dict wrapper

    >>> d = MaybeDict({'a': 'AAA'})
    >>> d['b'] = 'BBB'
    >>> d['a'], d['b'], d['z']
    ('AAA'?, 'BBB'?, <Nothing>)
    """

    def __init__(self, _dict):
        self.__dict = _dict

    def __getitem__(self, name):
        try:
            return Maybe(self.__dict[name])
        except KeyError:
            return Nothing()

    def __setitem__(self, name, value):
        self.__dict[name] = value


if __name__ == '__main__':
    import doctest
    doctest.testmod()
