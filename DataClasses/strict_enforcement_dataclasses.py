# Different ways for strict enforcement of dataclasses

from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str

u = User("oops", 123)
print(u)

'''
Dataclasses used the hints to generate fields, 
but didn't check types.
'''


# ----------------------------------------------------------------
# Ensuring Correctness

'''
1. Use static type checkers (compile-time safety)
Tools like mypy, pyright, or IDEs (PyCharm, VSCode) check your code before running.
'''

'''
2. Use __post_init__ for runtime validation
Dataclasses give you a hook that runs after __init__.
'''

@dataclass
class StrictUser:
    id: int
    name: str

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise TypeError(f"id must be int, got {type(self.id).__name__}")
        if not isinstance(self.name, str):
            raise TypeError(f"name must be str, got {type(self.name).__name__}")
        
try:
    u1 = StrictUser(10, "Aashish Raghav")
    print(u1)

    u2 = StrictUser("IIT2022010", "Aashish Raghav")
    print(u2)
except Exception as e:
    print(f"Exception : {e}")


'''
3. Use dataclass extensions with validation built-in
pydantic
 → auto type enforcement & validation
attrs
 → validators, converters
'''

from pydantic.dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
try:
    User("oops", 123)  # raises ValidationError at runtime
except Exception as e:
    print(f"Exception : {e}")


'''
4. Use libraries like beartype (runtime enforcement decorator)
You can slap @beartype on functions or classes, and it enforces type hints dynamically.
'''

from dataclasses import dataclass
from beartype import beartype # type: ignore

@beartype
@dataclass
class User:
    id: int
    name: str

try:
    User("oops", 123)  # TypeError at runtime
except Exception as e:
    print(f"Exception : {e}")
