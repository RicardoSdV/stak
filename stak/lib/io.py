import cPickle
cPickleDumps    = cPickle.dumps
cPickleLoad     = cPickle.load


def read(path):  # type: (str) -> str
    with open(path, 'r') as f:
        return f.read()

def write(path, _str):  # type: (str, str) -> None
    with open(path, 'w') as f:
        f.write(_str)

def readLines(path):  # type: (str) -> Lst[str]
    with open(path, 'r') as f:
        return f.readlines()

def writeLines(path, lines):  # type: (str, Itrb[str]) -> None
    with open(path, 'w') as f:
        f.writelines(lines)

def writeCPickle(path, data, protocol=cPickle.HIGHEST_PROTOCOL):
    with open(path, 'wb') as f:
        cPickleDumps(data, f, protocol)

def readCPPickle(path):
    with open(path, 'rb') as f:
        return cPickleLoad(f)