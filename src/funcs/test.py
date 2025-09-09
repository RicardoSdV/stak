import someCode
print someCode.__name__

from sys import _getframe

class A(object):
    @classmethod
    def clsmeth(cls):
        print cls

class B(A): pass

B().clsmeth()


# class Class(object):
#     def __meth(self):
#         pass
#
#     def meth(self, arg1=1):
#         print 'hasattr(self, "__meth")', hasattr(self, '__meth')
#         print 'self.__dict__', self.__dict__
#         func()
#         return 1
#
#
# def func():
#     frame = _getframe(1)
#     codeObj = frame.f_code
#
#     ## Frame
#     print 'f_locals', frame.f_locals
#     print 'f_globals', frame.f_globals
#     print
#
#     ## Code object
#     print 'co_argcount', codeObj.co_argcount
#     print 'co_cellvars', codeObj.co_cellvars
#     print 'co_code', codeObj.co_code
#     print 'co_consts', codeObj.co_consts
#     print 'co_filename', codeObj.co_filename
#     print 'co_firstlineno', codeObj.co_firstlineno
#     print 'co_flags', codeObj.co_flags
#     print 'co_freevars', codeObj.co_freevars
#     print 'co_lnotab', codeObj.co_lnotab
#     print 'co_name', codeObj.co_name
#     print 'co_names', codeObj.co_names
#     print 'co_nlocals', codeObj.co_nlocals
#     print 'co_stacksize', codeObj.co_stacksize
#     print 'co_varnames', codeObj.co_varnames
#
# obj = Class()
# obj.meth()

