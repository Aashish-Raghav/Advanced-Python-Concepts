from dataclasses import dataclass


# All parameters with their defaults
@dataclass(
    init=True,  # Generate __init__
    repr=True,  # Generate __repr__
    eq=True,  # Generate __eq__
    order=False,  # Generate __lt__, __le__, __gt__, __ge__
    unsafe_hash=False,  # Generate __hash__
    frozen=False,  # Make instances immutable
    match_args=True,  # Support pattern matching (Python 3.10+)
    kw_only=False,  # Make all fields keyword-only
    slots=False,  # Use __slots__ for memory efficiency
    weakref_slot=False,  # Add __weakref__ slot when using slots
)
class Example:
    field: str


# -------------------------------------------------------------------
# init parameter


@dataclass(init=True)
class withInit:
    name: str
    age: int


@dataclass(init=False)
class withoutInit:
    name: str
    age: int

    def __init__(self, name, age):
        print("Logic for custom init")
        self.name = name
        self.age = age


with_init = withInit("Alice", 42)
without_init = withoutInit("Alice", 42)
print(with_init)
print(without_init)
print(f"\n")


# -------------------------------------------------------------------
# repr parameter


@dataclass(repr=True)  # Default
class WithRepr:
    name: str
    secret: str


@dataclass(repr=False)
class WithoutRepr:
    name: str
    secret: str

    def __repr__(self):
        # Custom repr that hides sensitive data
        print("Logic for custom repr")
        return f"User(name='{self.name}', secret='***')"


with_repr = WithRepr("Alice", "password123")
without_repr = WithoutRepr("Bob", "secret456")

print(with_repr)  # WithRepr(name='Alice', secret='password123')
print(without_repr)  # User(name='Bob', secret='***')
print(f"\n")


# -------------------------------------------------------------------
# eq parameter


@dataclass(eq=True)  # Default
class WithEquality:
    name: str
    value: int


@dataclass(eq=False)
class WithoutEquality:
    name: str
    value: int


# With equality
a1 = WithEquality("test", 1)
a2 = WithEquality("test", 1)
print(a1 == a2)  # True

# Without equality (uses object identity)
b1 = WithoutEquality("test", 1)
b2 = WithoutEquality("test", 1)
print(b1 == b2)  # False (different objects)
print(b1 is b2)  # False
print(f"\n")


# -------------------------------------------------------------------
# frozen parameter


@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float


@dataclass(frozen=False)  # Default
class MutablePoint:
    x: float
    y: float


# Immutable dataclass
immutable = ImmutablePoint(1.0, 2.0)
print(immutable.x)  # 1.0

try:
    immutable.x = 3.0  # This will raise FrozenInstanceError
except Exception as e:
    print(f"Error: {e}")

# Mutable dataclass
mutable = MutablePoint(1.0, 2.0)
mutable.x = 3.0  # This works fine
print(mutable.x)  # 3.0

# Frozen dataclasses are hashable (can be used in sets/dicts)
immutable_points = {ImmutablePoint(1, 2), ImmutablePoint(3, 4)}
print(len(immutable_points))  # 2
print(f"\n")

"""
To prevent default behaviour of frozen dataclasses as hashable
1. __hash__ = None , override the method
2. set eq and unsafe_hash parameter as False,
but 2nd doesn't work because if we don't have eq then it inherits
from base object which is id comparsion and also its hash which
is on object id, so remain hashable.
Need to explicitly mark hash function as none to obtain this behaviour 
"""


# -------------------------------------------------------------------
# order parameter


@dataclass(order=True)
class Student:
    name: str
    grade: float
    age: int


students = [Student("Alice", 3.8, 22), Student("Bob", 3.6, 21), Student("Bob", 3.2, 23)]

# Sorting works automatically
sorted_students = sorted(students)
for student in sorted_students:
    print(f"{student.name}: {student.grade}")

# Output (lexicographic order by all fields):
# Alice: 3.8
# Bob: 3.6
# Charlie: 3.9

# You can also use comparison operators
alice = Student("Alice", 3.8, 22)
bob = Student("Bob", 3.6, 21)
print(alice > bob)  # False (Alice comes before Bob alphabetically)
print(f"\n")


# -------------------------------------------------------------------
# slots parameter

@dataclass(slots=True)
class EfficientPoint:
    x: float
    y: float

@dataclass(slots=False)  # Default
class RegularPoint:
    x: float
    y: float

from pympler import asizeof # type: ignore

efficient = EfficientPoint(1.0, 2.0)
regular = RegularPoint(1.0, 2.0)

print(asizeof.asizeof(efficient))  # e.g., ~56 bytes
print(asizeof.asizeof(regular))    # e.g., ~112 bytes


# With slots, you can't add new attributes dynamically
try:
    efficient.z = 3.0  # This will raise AttributeError
except AttributeError as e:
    print(f"Slots restriction: {e}")

# Regular dataclass allows dynamic attributes
regular.z = 3.0  # This works
print(regular.z)  # 3.0


'''
RegularPoint object
 ├── header (refcount, type)
 ├── pointer to dict ----------------┐
                                     │
dict (hash table)                    │
 ├── entry: "x" → pointer ---------->│ int(1)
 ├── entry: "y" → pointer ---------->│ int(2)
'''

# vs

'''
EfficientPoint object
 ├── header (refcount, type)
 ├── slot[0] → pointer -------------> int(1)
 ├── slot[1] → pointer -------------> int(2)

'''