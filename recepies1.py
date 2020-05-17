from socket import socket, AF_INET, SOCK_STREAM
from functools import partial


class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None

    '''
            ---------------------- Explanation ----------------------
    
    The main reason of this class is it opens a socket connection and closes it.
    By default it does nothing. The connection is made on demand with the use of
    context manager or with keyword, for example:
    
            ----------------------------------------------------------
    '''

    # if __name__ == '__main__':
    #     conn = LazyConnection(('www.python.org', 80))
    #     # Connection is still closed
    #     with conn as c:
    #         # __enter()__ was called, connection opened
    #         c.send(b'GET /index.html HTTP/1.0\r\n')
    #         c.send(b'Host: www.python.org\r\n')
    #         c.send(b'\r\n')
    #         resp = b''.join(iter(partial(c.recv, 8192), b''))
    #         print(resp)
    #         # conn.__exit__() connection closed

    '''
    The main reason behind building a context manager is that you write code that is 
    surrounded by block of instructions of with(context manager).
    When the with instructions are first given to the interpreter __enter__() method
    is being called. In the exit method __exit__() is being called.
    The code within with block will be executed one way or another even if there are exceptions
    __exit__() can use the information of a exception or either ignore it doing nothing
    and returning None as a result. If __exit__() returns True the exception vanishes and
    the program runs as if nothing has happened.
    
    Currently we are allowed to have a single socket connection. As seen in code, if
    more than one connection is done we raise a RuntimeError.Of course, we can go around
    and import support for multiple socket connections
    '''


class LazyConnection2:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connections.pop().close()


# if __name__ == '__main__':
#     conn = LazyConnection2(('www.python.org', 80))
#     with conn as conn1:
#         conn1.send(b'GET /index.html HTTP/1.0\r\n')
#         conn1.send(b'Host: www.python.org\r\n')
#         conn1.send(b'\r\n')
#         resp = b''.join(iter(partial(conn1.recv, 8192), b''))
#         print('First response {}'.format(resp))
#         print('-'*10)
#         with conn as conn2:
#             conn2.send(b'GET /index.html HTTP/1.0\r\n')
#             conn2.send(b'Host: www.python.org\r\n')
#             conn2.send(b'\r\n')
#             resp = b''.join(iter(partial(conn2.recv, 8192), b''))
#             print('Second response {}'.format(resp))

'''
Context managers are used more often in programs that need to control resources like files, network connections
or blocking. The key point of these resources is that they need to be closed or freed in order to work correctly.
'''

# ------------------------------------------ Part 2 ------------------------------------------------------

'''
    If you have million of objects that act as simple data structures, you can use __slots__ to significantly
    decrease the memory usage of your programs.    
'''


class Date:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    '''
        When you use slots, instead of converting each element into a dictionary, python stores them inside a 
        specific data type with fixed size similar to tuple or a list. Attributes specified inside __slots__
        are linked to a specific index of a variable. Only side effect is you can't add new attributes and will
        be able to use only those specified inside __slots__
    '''

    # ------------------------------------------ Part 3 ------------------------------------------------------

    '''
        When creating many classes that are used as data structures it can be eased by defining a temp buffer
        for data types that will be the base of your class constructor
    '''

    # class Structure:
    #     _fields = []
    #
    #     def __init__(self, *args):
    #         if len(args) != len(self._fields):
    #             raise TypeError('Expected {} of arguments'.format(len(self._fields)))
    #         for name, value in zip(self._fields, args):
    #             setattr(self, name, value)
    #
    #
    # if __name__ == '__main__':
    #     class Person(Structure):
    #         _fields = ['first_name', 'last_name']
    #
    #
    #     p = Person('Andrew', 'Anderson')

    '''
        If you decide to give keyword argument support then there are few ways to realize that approach.
        One way is to reflect keyword arguments so they would correspond to attribute names defined in _fields.
        Example:
    '''

    # class Structure:
    #     _fields = []
    #
    #     def __init__(self, *args, **kwargs):
    #         if len(args) != len(self._fields) and (len(args) + len(kwargs) != len(self._fields)):
    #             raise TypeError('Expected {} of arguments'.format(len(self._fields)))
    #         for name, value in zip(self._fields, args):
    #             setattr(self, name, value)
    #
    #         for name in self._fields[len(args):]:
    #             setattr(self, name, kwargs.pop(name))
    #
    #             # Check leftover arguments
    #         if kwargs:
    #             raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

    # if __name__ == '__main__':
    #     class Person(Structure):
    #         _fields = ['first_name', 'last_name', 'address']

    # p1 = Person('Andrew', 'Anderson', 'someStreet 5-43')
    # p2 = Person('Andrew', 'Anderson', address='someStreet 5-43')
    # p3 = Person('Andrew', last_name='Anderson', address='someStreet 5-43')
    # p3 = Person('Andrew', last_name='Anderson', address='somestreet 5')
    # print(p2.address)

    '''
        Another way is to use keyword arguments as a resource of adding additional attributes that weren't defined
        in _fields[]
    '''

    # class Structure:
    #     _fields = []
    #
    #     def __init__(self, *args, **kwargs):
    #         if len(args) != len(self._fields) and (len(args) + len(kwargs) != len(self._fields)):
    #             raise TypeError('Expected {} of arguments'.format(len(self._fields)))
    #
    #         for name, value in zip(self._fields, args):
    #             setattr(self, name, value)
    #             # if extra_args, add them
    #         extra_args = kwargs.keys() - self._fields
    #         for name in extra_args:
    #             setattr(self, name, kwargs.pop(name))
    #         if kwargs:
    #             raise TypeError('Duplicate values for {}'.format(', '.join(kwargs)))
    #
    #
    # if __name__ == '__main__':
    #     class Stock(Structure):
    #         _fields = ['name', 'shares', 'price']
    #
    #
    #     s1 = Stock('ACME', 50, 91.1)
    #     s2 = Stock('ACME', 50, 91.1, date='8/2/2012')
    #     print(s2.name)

    # ------------------------------------------ Part 4 ------------------------------------------------------

    '''
        You need to create a data structure, but you need to limit definition of attributes that can be assigned 
        to a class.
        Let's say, you need to create type checking for specific attributes. In order to do that, you need to
        customize attribute setup for each attribute.
    '''


#
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


# Decorator for type checking
class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected type {}'.format(self.expected_type))
        super(Typed, self).__set__(instance, value)


# # Decorator for type checking
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expectec >= 0')
        super().__set__(instance, value)


# Decorator for type checking
class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise ValueError('Expected size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super().__set__(instance, value)

    '''
        These classes should be looked as basic building blocks from which you create your data model or type system
    '''


#
class Integer(Typed):
    expected_type = int


class UnsignedInteger(Integer, Unsigned):
    pass


class Float(Typed):
    expected_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    expected_type = str


class SizedString(String, MaxSized):
    pass

    '''
        Using these types, we can define our custom class
    '''

    # class Stock:
    #     name = SizedString('name',size=8)
    #     shares =UnsignedInteger('shares')
    #     price = UnsignedFloat('price')
    #
    #     def __init__(self,name, shares, price):
    #         self.name = name
    #         self.shares = shares
    #         self.price = price

    # TODO: create some examples

    '''
        There are a few other ways to make specification limit for a class.
        One of them is to use decorator class
    '''
    #
    # def check_attribute(**kwargs):
    #     def decorate(cls):
    #         for k, v in kwargs.items():
    #             if isinstance(v, Descriptor):
    #                 v.name = k
    #                 setattr(cls, k, v)
    #             else:
    #                 setattr(cls, k, v(k))
    #         return cls
    #     return decorate
    # #
    # #
    # @check_attribute(name=SizedString(size=8),
    #                  shares=UnsignedInteger,
    #                  price=UnsignedFloat)
    #
    # class Stock:
    #     def __init__(self, name, shares, price):
    #         self.name = name
    #         self.shares = shares
    #         self.price = price

    '''
        Another way is to use metaclass
    '''

    # class CheckedMeta(type):
    #     def __new__(cls, clsname, bases, methods):
    #         for key, value in methods.items():
    #             if isinstance(value, Descriptor):
    #                 value.name = key
    #         return type.__new__(cls, clsname, bases, methods)
    #
    #
    # class Stock(metaclass=CheckedMeta):
    #     name = SizedString(size=8)
    #     shares = UnsignedInteger()
    #     price = UnsignedFloat()
    #
    #     def __init__(self, name, shares, price):
    #         self.name = name
    #         self.shares = shares
    #         self.price = price

    '''
        In Descriptors base class is a method __set__(), but not __get__(). If
        descriptor isn't doing anything but extract the value with the same name
        from the dict there is no need to define __get__() and further more it makes
        the program slower
    '''

    # ------------------------------------------ Part 5 ------------------------------------------------------

    '''
        If you need to crete a custom class that copies the behaviour of a data structure like list or dictionary,
        but you aren't completely sure what methods you need to define.
        Lets say you need to create a class that supports iteration. For that, we can inherit from 
        collections.Iterable 
    '''

    # from collections import Iterable
    #
    #
    # class Item(Iterable):
    #     pass
    #
    # if __name__ == '__main__':
    #     c = Item()
    # Print error, can't instantiate class with iter

    '''
        Of course, if you want to make your class iterable you can simply override __iter__(). Lets take a look at
        another example
    '''


from collections import Sequence
import bisect


class SortedItem(Sequence):
    def __init__(self, sequence=None):
        self._items = sorted(sequence) if sequence is not None else []

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def add(self, other):
        bisect.insort(self._items, other)


if __name__ == '__main__':
    items = SortedItem([10, 43, 3])
    print(list(items))
    print('-' * 10)
    print(items[0])
    print('-' * 10)
    print(items[-1])
    print('-' * 10)
    items.add(2)
    print(list(items))
    print('-' * 10)
    print(items[1:4])
    print('-' * 10)
    print(3 in items)
    print('-' * 10)
    print(len(items))
    print('-' * 10)
    for i in items:
        print(i)

    '''
        As you can see, example of SortedItem behaves like usual Sequence and supports all other operations
        including indexing, iteration, len(), in checking and even slicing. bisect module, used in this 
        recipe gives a comfortable support of element sorting inside a list. Since bisect.insort() inserts
        elements inside of a list, the sequence stays sorted.
    '''
