
def autoName():
    # Get caller frame
    from sys import _getframe
    frame = _getframe(1)
    funcName = frame.f_code.co_name
    fGlobals = frame.f_globals

    if funcName.startswith('__'):
        for name, obj in fGlobals.iteritems():
            if name.startswith('_'):
                mangled = name + funcName
            else:
                mangled = '_' + name + funcName

            if hasattr(obj, mangled):
                print obj.__name__ + '.' + funcName
                break
    else:
        for obj in fGlobals.itervalues():
            if hasattr(obj, funcName):
                print obj.__name__ + '.' + funcName
                break

class Class(object):
    @staticmethod
    def sMeth():
        autoName()

    @classmethod
    def cpsMeth(cls):
        cls.__psMeth()

    @staticmethod
    def __psMeth():
        autoName()

Class.sMeth()
Class.cpsMeth()
