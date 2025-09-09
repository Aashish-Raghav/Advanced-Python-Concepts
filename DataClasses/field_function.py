from dataclasses import dataclass, field

'''
items [] is created once at class definition time, not every time you 
create an instance. Dataclasses (and pydantic too) explicitly forbid mutable 
defaults like [], {}, set(), proactively raise an error instead of letting it 
happen silently. This is a safety feature.

Something like this happens
def __init__(self, items=[]):   # <-- default baked in!
    self.items = items

'''
# @dataclass
# class WrongExample:
#     items : list[str] = [] # Shared among all objects, WRONG

# w1 = WrongExample()
# w2 = WrongExample()
# print(w1.items is w2.items)


@dataclass
class CorrectExample:
    items : list[str] = field(default_factory=list)

c1 = CorrectExample()
c2 = CorrectExample()
print(c1.items is c2.items)

'''
NOTE:
When you use dataclass, Python's codegen logic does something like:
If the field has a simple default (x: int = 42):
→ emit def __init__(..., x=42).

If the field has a default_factory:
→ emit def __init__(..., x=_MISSING), and inside check:

def __init__(self, items=_MISSING):
    if items is _MISSING:
        self.items = list()   # <-- call factory at runtime
    else:
        self.items = items

'''