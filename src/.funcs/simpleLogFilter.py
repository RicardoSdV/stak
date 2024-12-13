names = (
    'name1.log',
)

lookingFor = (
    'lookingFor1',
)

def filterLines(lines):
    for line in lines:
        for thing in lookingFor:
            if thing in line:
                yield line
                break

for name in names:
    with open(name, 'r') as _file:
        lines = _file.readlines()

    with open('filtered' + '_' + name, 'w') as _file:
        _file.writelines(filterLines(lines))
