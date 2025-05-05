from copy import copy
from functools import partial
from os.path import join

from src.stak_func.stak.z_utils import read, write, packageName

if __name__ == '__main__':
    raise Exception("Don't run this file, for autoSettings run injectors.py")

settingsPath   = join(packageName, 'block01_settings.py')
settingObjPath = join(packageName, 'block02_settingObj.py')

readSettings   = partial(read, settingsPath)
readSettingObj = partial(read, settingObjPath)

writeSettings   = partial(write, settingsPath)
writeSettingObj = partial(write, settingObjPath)


settingsLines = readSettings()


from src.stak_func.stak import block01_settings
settingsNames = [
    name
    for name in block01_settings.__dict__
    if not name.startswith('__')
]
slottables = copy(settingsNames)  # For export

selfishLines = []
for line in settingsLines:
    if ' = ' in line and any(name in line for name in settingsNames):
        selfishLines.append('self.' + line)
    else:
        selfishLines.append(line)

indentedLines = [
    '        ' + line if line != '\n' else line
    for line in selfishLines
]

settingObjLines = readSettingObj()

for i, line in enumerate(settingObjLines):
    if line == '    def __init__(self):\n':
        initInitIndex = i + 1

    if line == '        ## Init finit (do not delete this comment)\n':
        initFinitIndex = i - 1
        break

emptyInitSettingObjLines = settingObjLines[:initInitIndex] + settingObjLines[initFinitIndex:]

rewrittenSettingObjLines = emptyInitSettingObjLines

i = initInitIndex + 1
while indentedLines:
    newLine = indentedLines.pop()
    if '"""' in newLine:
        continue

    rewrittenSettingObjLines.insert(i, newLine)

writeSettingObj(rewrittenSettingObjLines)
