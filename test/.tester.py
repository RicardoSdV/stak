## Test settings
from test.t_settingReloader import runSettingReloadingTest
testStak      = 0
testTrace     = 0
testIntercept = 0
testReloader  = 0
traceStak     = 0
fixedTestRuns = 40
rndTestRuns   = 10

runRunTests = testStak or testIntercept


from itertools import repeat
from random import randint

from stak import *

from test.t_omrols import runStakTest
from test.t_interceptor import runInterceptTest
from test.t_trace import runTraceTest


def runTests():
    if not testStak:
        return

    for _ in repeat(None, fixedTestRuns):
        for _ in repeat(None, randint(1, rndTestRuns)):

            if testStak:
                runStakTest()

            if testIntercept:
                runInterceptTest()


if traceStak:
    setTrace()

runTests()

if traceStak:
    delTrace()

if testTrace:
    runTraceTest()

if testReloader:
    runSettingReloadingTest()

import code
shell = code.InteractiveConsole(globals())
shell.interact()
