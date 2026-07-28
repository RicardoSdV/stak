from . import config, state
from .utils.log import ERROR
from .lib import deepCopy, sysModules


def reloadConfig():
    oldConfig = deepCopy(state.config)
    newConfig = deepCopy(reload(config).__dict__)

    state.config.clear()
    state.config.update(newConfig)

    # TODO: There needs to be some stuff done when certain configs change


def _jamInterfaceToBuiltins(callFromShellInterface):
    if not state.config['jamInterfaceToBuiltins']:
        return

    reloading = __package__ in sysModules
    builtins = __builtins__.__dict__
    _globals = globals()

    for name in callFromShellInterface:
        if reloading or name not in builtins:
            builtins[name] = _globals[name]
        else:
            ERROR('COLLISION! While jamming interface into builtins, name=%s' % name)

    if state.config['isDev'] and 'stak' not in builtins:
        builtins['stak'] = sysModules[__name__]
