"""
In the quest for the most simple event system ever, events are functions which are named with the event name,
event handlers are functions which are named -> {eventName}_{handlerName}. In this way all events, what handlers
they call & what order they are in can be simply & explicitly defined in this file.

So, what is an event even? why not just call the handlers whenever they need to be called and that's it? Well,
its kind of comfortable to have certain notable events explicitly defined without having to dig through the code
to see when they happen is the only reason I can think of. But im not yet convinced this file will keep existing.
"""

from .block00_autoImports import *


def onStakLoads():
    onStakLoads_compileStakC()
    onStakLoads_replaceCPlaceholders()
    onStakLoads_setSettingsToC()
    onStakLoads_interceptLoggers()
    onStakLoads_runInjectors()

def onStakPreReload():
    onStakPreReload_restoreLoggers()

def onStakPostReload():
    onStakPostReload_interceptLoggers()

def onSettingsReload(oldSettings, newSettings):
    onSettingsReload_setSettingsToC()
    onSettingsReload_reIntercept(oldSettings, newSettings)
    onSettingsReload_updateTracing(oldSettings, newSettings)
