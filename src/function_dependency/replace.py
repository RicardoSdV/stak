def replace(func):
    print 'replace'
    def times10(x):
        print 'times10'
        return x * 10
    return times10

@replace
def plus1(x):
    print 'myFunction'
    return x + 1

print 'preCall'
print plus1(5)
print 'postCall'
