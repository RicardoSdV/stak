from ..lib import mathFloor, mathLog10

def roundToSigFigs(x, sigFigs):
    if x == 0:
        return 0
    return round(x, sigFigs - int(mathFloor(mathLog10(abs(x)))) - 1)
