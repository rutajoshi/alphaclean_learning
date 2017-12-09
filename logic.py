"""
Module defines basic logical building blocks for writing rules
"""


#boolean logic
def implies(a,b):
    return (not a) or b

def xor(a,b):
    return (a and not b) or (not a and b)

def iff(a,b):
    return implies(a,b) and implies(b,a)





#tuple logic
def eq(a,b, attr):
    return _op( a, b, attr, lambda s,t: s == t)

def neq(a,b, attr):
    return _op( a, b, attr, lambda s,t: s != t)

def gt(a,b, attr):
    return _op( a, b, attr, lambda s,t: s > t)

def lt(a,b, attr):
    return _op( a, b, attr, lambda s,t: s < t)


def _op(a , b, attr, comparator):

    if isinstance(a, tuple) and \
        isinstance(b, tuple):

        return comparator(a[attr], b[attr])

    elif isinstance(a, tuple):

        return comparator(a[attr],b)

    else:
        return comparator(a,b[attr])



#format operators
def isFloat(a,attr):
    try:
        float(a[attr])
        return True
    except:
        return False