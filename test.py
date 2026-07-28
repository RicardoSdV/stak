## Test settings
testStak      = 1
testTrace     = 0
testIntercept = 0
testReloader  = 0
traceStak     = 0
fixedTestRuns = 40
rndTestRuns   = 10

runRunTests = testStak or testIntercept


import sys
from itertools import repeat
from random import randint

import stak
from stak import *

from test.t_omrols import runStakTest
from test.t_interceptor import runInterceptTest
from test.t_trace import runTraceTest
from test.t_settingReloader import runSettingReloadingTest

sys.dont_write_bytecode = True


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
shell = code.InteractiveConsole(stak.__dict__)
shell.interact()
