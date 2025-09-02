# metaclass for creating singleton classes only

# using type inheritance
class SingletonMeta(type):
    _instances = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args,**kwargs)
        return cls._instances[cls]
    
class Database(metaclass=SingletonMeta):
    pass

class Logger(metaclass=SingletonMeta):
    pass

d1 = Database()
d2 = Database()
print(d1 is d2)

l1 = Logger()
l2 = Logger()
print(l1 is l2)


# using function as metaclass

def debug_meta(name, bases, attrs):
    print(f"Creating class {name}")
    print(f"Base classes: {bases}")
    print(f"Attributes: {list(attrs.keys())}")

    return type(name, bases, attrs)


class DebugClass(metaclass = debug_meta):
    def method(self):
        pass

d = DebugClass()

