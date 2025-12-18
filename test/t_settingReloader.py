from traceback import print_exc

def runSettingReloadingTest():
    path = stak.getAbsPathForBlockName('settings')
    with open(path, 'r') as f:
        lines = f.readlines()
    lines.append('testSetting = 1\n')

    lines.append('def returnTestSetting():\n')
    lines.append('    return testSetting\n')

    with open(path, 'w') as f:
        f.writelines(lines)

    try:
        stak.reloadStak()

        lines[-3] = 'testSetting = 2\n'

        with open(path, 'w') as f:
            f.writelines(lines)

        stak.reloadSettings()
        num = stak.returnTestSetting()
        assert num == 2, 'num = %s' % num

    except Exception as e:
        print_exc()

    finally:
        lines = lines[:-3]
        with open(path, 'w') as f:
            f.writelines(lines)




