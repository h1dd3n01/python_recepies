# ----------------- Visitor data structure without recursion ------------------
'''
    You write code that iterates through a deeply nested structure and brakes due to
    exceeding the limit of recursion. Example of how to get rid of recursion but still
    keeping the visitor pattern design.
    Generators can be used smartly to get around recursion of an algorithm of a tree or
    search.
'''

import types


class Node:
    pass


class NodeVisitor:
    def visit(self, node):
        stack = [node]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    '''
                        Resumes the execution and "sends" a value into the generator function.
                        The value argument becomes the result of the current yield expression.
                        The send method returns the next value yielded by the generator,
                        or raises StopIteration if the generator exits without yielding another value.
                    '''
                    stack.append(last.send(last_result))
                    last_result = None
                elif isinstance(last, Node):
                    stack.append(self._visited(stack.pop()))
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()
        return last_result

    def _visited(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))


'''
                    You have a program that cycles a structure, and memory problems occur   
    Simple example is a tree, where the parent targets the child and the child back to the parent. When you work with
    that kind of a structure you need to consider in making one of the types a wekref, using weakref module.     
'''

import weakref


class Node:
    def __init__(self, value):
        self.value = value
        self._parent = None
        self.children = []

    def __repr__(self):
        return 'Node({!r:})'.format(self.value)

    # Property that controls the parent
    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def add_child(self, node):
        self.children.append(node)
        self._parent = self


'''
        You want to return the a cached classes previous element that was created with the same arguments.
        The problem that this recipe solves, is it creates only one example of a class with specific arguments.
        Lets take logging library for example.
    
    >>> import logging

    >>> a = logging.getLogger('foo')
    >>> b = logging.getLogger('bar')
    >>> a is b
    False
    >>> c = logging.getLogger('foo')
    >>> a is c
    True
    
        In order to get the same behaviour in a class, you need to use a fabrical function that is separated from the class
'''


class Spam:
    def __init__(self, name):
        self.name = name


import weakref

_spam_cache = weakref.WeakValueDictionary()


def get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = name
    else:
        return _spam_cache[name]

    #        -------------------------------  Another approach -------------------------------------------


import weakref


class Spam:
    _spam_cache = weakref.WeakValueDictionary()

    def __new__(cls, name):
        if name in cls._spam_cache:
            return cls._spam_cache[name]
        else:
            self = super().__new__()
            cls._spam_cache[name] = self
            return self

    def __init__(self, name):
        print('Initializing Spam')
        self.name = name

    '''
        Problem with this code resides that whenever you call, __init__ is return always a value without considering
        is the value cached or not.
        
        >>> s = Spam('Dave')
        Initializing Spam
        >>> t = Spam('Dave')
        Initializing Spam
        >>> s is t
        True
        >>>
        
        Using weakref plays a vital role in this recipe considering garbage collection.The logic is following
        you want to use a example in memory till it is used somewhere, WeakRefDictionary holds elements that are used
        somwhere, the value keys are vanished when example stops being used.
        
        
        >>> a = get_spam('foo')
        >>> b = get_spam('bar')
        >>> c = get_spam('foo')
        >>> list(_spam_cache)
        ['foo', 'bar']
        >>> del a
        >>> del c
        >>> list(_spam_cache)
        ['bar']
        >>> del b
        >>> list(_spam_cache)
        []
        >>>
        
        Even tho this recipe is good and enough for big programs tho there are some better approaches.
    '''


import weakref


class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
            return s

    def clear(self):
        self._cache.clear()


class Spam:
    manager = CachedSpamManager()

    def __init__(self, name):
        self.name = name

    def get_spam(name):
        return Spam.manager.get_spam(name)
