import ctypes
class PyObject(ctypes.Structure):
    _fields_ = [("ob_refcnt", ctypes.c_long),
                ("ob_type", ctypes.c_void_p)]

x = object()
y = x
z = x
addr = id(x)
obj = PyObject.from_address(addr)

print("Refcount:", obj.ob_refcnt) # Useful in Garbage Collection
print("Type pointer:", hex(obj.ob_type))
print()


# -------------------------------------------------------------

import sys

x = []
y = x
z = y
print(f"refCount({x}): {sys.getrefcount(x)}")  # e.g., 2
print()

'''
This number will always look 1 higher than you expect, because 
calling sys.getrefcount(x) temporarily creates another reference 
(x passed as argument).
'''


x = 10
y = 10
z = 10
print(f"refCount({x}): {sys.getrefcount(x)}") 
print()

'''
Why -1?

In CPython, some immortal objects (like small ints, None, True, etc.) use reference count tricks:
They may store a fake refcount (like -1) to indicate “immortal object — never deallocate”.
This optimization was introduced in newer Python versions (3.11+).
So your 10 object probably has ob_refcnt = -1 in memory, meaning "don't free this".
This would interpret the signed refcount field (-1) as 4294967295
Till which number do we have this ?
'''


def func():
    i = 0
    while True:
        yield i
        i+=1

for x in func():
    if sys.getrefcount(x) != 4294967295:
        print(f'Number: {x}, refCount : {sys.getrefcount(x)} ')
        break



print(sys.getsizeof([1,2,3]))
print(sys.getsizeof([1.0,"Hellow","world"])) 
'''
That 88 is just the list container itself (header, capacity, pointers).
It does not include the size of the elements inside (1, 2, 3).
So, to get the "real" size of the whole structure, you'd have to traverse it manually.
'''


from pympler import asizeof # type: ignore
print(asizeof.asizeof([1,2,3]))
print(asizeof.asizeof([1.0,"Hellow","world"]))
'''
asizeof walks the entire object graph recursively.
It includes the list, plus the integers, plus any substructures.
Avoids double-counting shared references.
'''