from .block00_autoImports import *

# TODO: Ok, so, we need to be able to stak both classes and instances with some sort of mixin, or decorator, or similar


# Mixin to debug event classes
class DebugEvent(object):
    def __init__(self, debugInstanceName='NAME ME YOU LAZY BASTARD!', *args, **kwargs):
        omrolocsalad()
        super(DebugEvent, self).__init__(*args, **kwargs)
        self.__name = debugInstanceName

    def __call__(self, *args, **kwargs):
        omrolocsalad()
        super(DebugEvent, self).__call__(*args, **kwargs)

    def __iadd__(self, other):
        omrolocsalad()
        super(DebugEvent, self).__iadd__(other)
