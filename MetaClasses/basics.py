# This example demonstrates the use of metaclass concept in Python.
# We dynamically create a class using the built-in 'type' metaclass.

def bark_method(self):
    return "Woof!"

# Dynamically create a Dog class using type() metaclass
# The class has one method: bark
Dog = type("Dog", (), {"bark": bark_method})

# Instantiate the Dog class
dog = Dog()

# Call the bark method and print
print(dog.bark())