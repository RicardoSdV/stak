from traceback import print_stack



KEY = 'gun/canShoot'


class DebugDict(dict):

    def __setitem__(self, key, value):
        if KEY == key:
            print_stack()
            if key in self:
                print "[DebugDict] Updating key: {} from {} to {}".format(key, self[key], value)
            else:
                print "[DebugDict] Adding key: {} with value: {}".format(key, value)
        super(DebugDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        if KEY == key:
            print_stack()
            if key in self:
                print "[DebugDict] Removing key: {} with value: {}".format(key, self[key])
            else:
                print "[DebugDict] Attempted to remove non-existent key: {}".format(key)
        super(DebugDict, self).__delitem__(key)

    def update(self, *args, **kwargs):
        _dict = dict(*args, **kwargs).iteritems()
        if KEY in _dict:
            print_stack()
            for key, value in _dict:
                if key in self:
                    print "[DebugDict] Updating key via update(): {} from {} to {}".format(key, self[key], value)
                else:
                    print "[DebugDict] Adding key via update(): {} with value: {}".format(key, value)
        super(DebugDict, self).update(*args, **kwargs)

    def pop(self, key, *args):
        if KEY == key:
            print_stack()
            if key in self:
                print "[DebugDict] Popping key: {} with value: {}".format(key, self[key])
            else:
                print "[DebugDict] Attempted to pop non-existent key: {}".format(key)
        return super(DebugDict, self).pop(key, *args)

    def setdefault(self, key, default=None):
        if KEY == key:
            print_stack()
            if key in self:
                print "[DebugDict] Key {} already exists with value {}, setdefault() did nothing".format(key, self[key])
            else:
                print "Key {} not found, setting default value: {}".format(key, default)
        return super(DebugDict, self).setdefault(key, default)