from dataclasses import dataclass


@dataclass(eq=False)
class Person:
    name: str
    age: int
    email: str


person1 = Person("Alice", 21, "alice@example.com")
person2 = Person("Alice", 21, "alice@example.com")

st = set()
print(person1)
print(person1 == person2)

for i in range(20, 30):
    st.add(Person(f"Alice_{i-20}", i, f"alice_{i-20}@gmail.com"))

print(st)
