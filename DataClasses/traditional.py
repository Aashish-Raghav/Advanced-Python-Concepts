class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person({self.name},{self.age},{self.email})"

    def __eq__(self, value):
        if not isinstance(value, Person):
            return False

        return (
            self.name == value.name
            and self.age == value.age
            and self.email == value.email
        )

    def __hash__(self):
        return hash((self.name, self.age, self.email))


person1 = Person("Alice", 21, "alice@example.com")
person2 = Person("Alice", 21, "alice@example.com")

st = set()
print(person1)

print(person1 == person2)

for i in range(20, 30):
    st.add(Person(f"Alice_{i-20}", i, f"alice_{i-20}@gmail.com"))

print(st)


""" 
Note: Making Custom Objects "Hashable":
By default, custom objects are hashable if they don't override __eq__. 
However, if you implement __eq__ but not __hash__, your objects 
become unhashable, meaning they cannot be used as keys 
in dictionaries or elements in sets. Implementing __hash__ 
makes your custom objects compatible with these data structures.
"""
