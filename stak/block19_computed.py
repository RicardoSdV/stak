""" Computed: Constants that are computed once the package is loaded. """

from .block00_autoImports import *

gSpace = globals()

lenPyExt       = len(pyExt)
nLenPyExt      = -lenPyExt
lenPycExt      = len(pycExt)
lenBlockPrefix = len(blockPrefix)

# os does not hold the correct path char for certain programs, when inspecting frames,
# for saving should os.path.join, but for frame ops use pathSplitChar.
pathSplitChar = '/' if '/' in sysGetFrame(0).f_code.co_filename else '\\'

splitPackageDotPath = __name__.split('.')[:-1]
packageName = splitPackageDotPath[-1]

absPackagePath = osPathDirName(osPathAbsPath(__file__))
lenAbsPackagePath = len(absPackagePath)
