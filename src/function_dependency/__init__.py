"""
So, I find circular imports annoying, the only legitimate reason to create different
files should be purely for programmer comfort, not because of dumb ass circular imports,
actually defining the imports within each function I think is not such a terrible idea
since locality of behaviour is good, but sadly is pretty slow, so the idea of this mini
project is to attempt to do in-function imports less bad, so, the fastest way of calling
a name from outside the function inside the function is to make it a default arg,
so the question is if it is possible to write a decorator which defines a series of
dependencies which are imported on first call of a function and set to its default
arguments, where after the first call the function which replaces default args is
substituted somehow with the original function, such that effectively after the first
call it is effectively as if the function is just importing default args on file import
but avoiding the circular dependencies.

ogFunc: does the thing
repFunc: replaces kwargs, calls og func

on Import:
    - Replace og Func with


"""


