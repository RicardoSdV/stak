from sys import _getframe

from . import interface as i
from . import noface as n


class Interface(object):
    def __init__(self, omrolocs):
        self.omrolocs = omrolocs


interface = Interface(i.omrolocs)
noface = Interface(n.omrolocs)


silenced = {
    r'C:\prjs\stak\src\testImports\silenced.py': 1,
    r'C:\prjs\stak\src\testImports\loud.py': 0,
}

def cios():
    """ Conditional importing of stak """
    frame = _getframe(1)
    filePath = frame.f_code.co_filename

    if filePath in silenced and silenced[filePath]:
        return noface
    return interface





