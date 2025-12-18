from stak import *
from stak import labelLogs
from test.t_someCode import SomeClass

def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Interface(object):
    def testCallerOfCaller(self):
        raise NotImplementedError()

class Ganny(object):
    pass

class Daddy(Ganny):
    def forMethNameDupBug(self):
        omrolocs()

    @decorator
    def test(self, someLocalParam=69):
        someOtherLocal = 'yesDaddy'
        omrolocsalad(someDatumForExtraLogging='420')
        somePostOmrolocsaladLocal = 'yes this is post the salad'
        omrolocs()
        ffad()
        ffad(someDatum=[1, 2, 3, 4])
        ffad(pretty=False, someDatum=[1, 2, 3, 4], someDatum2=[1, 2, 3, 4])
        omropocs()
        ffadal()
        labelLogs()
        ffad(SOME_SEPARATOR='================================================================================================')

    @property
    def __privProp(self):
        return self.test()

    def __testCaller(self):
        self.__privProp

    def testCaller(self):
        ffad(someDatum=[1, 2, 3, 4], someDatum2=[1, 2, 3, 4])
        localVar = 1
        self.__testCaller()

class SomeCls(Daddy, Interface):
    @property
    def propCallerOfCallerOfCaller(self):
        return self.testCallerOfCaller()

    def testCallerOfCaller(self):
        self.testCaller()

class Bro(Daddy):
    pass

class Dawg(SomeCls):
    pass

class ParentStatConf(object):
    @staticmethod
    def statMeth():
        ParentStatConf.__statMeth()

    @staticmethod
    def __statMeth():
        Outcast.classMeth()

class SomeSomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMeth():
        pass

class Outcast(ParentStatConf):
    def __init__(self):
        self.statMeth()

    @classmethod
    def classMeth(cls):
        cls.__classMeth()

    @classmethod
    def __classMeth(cls):
        Dawg().propCallerOfCallerOfCaller

class SomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMeth():
        pass

SomeClass().someMeth()

class OutcastSon(Outcast):
    pass

def func():
    OutcastSon()

class OldStyle:
    @staticmethod
    def oldStyleStaticMeth():
        func()

    @classmethod
    def oldStyleClassMeth(cls):
        cls.oldStyleStaticMeth()

    def oldStyleInstanceMeth(self):
        self.oldStyleClassMeth()

class NameDup(object):
    def nameDup(self):
        omrolocsalad()

def func2():
    a, b = 1, 2
    omrolocsalad()
    ffad(a=a, b=b)
    ffadal()


def runStakTest():
    OldStyle().oldStyleInstanceMeth()
    NameDup().nameDup()
    func2()
    Bro().forMethNameDupBug()
