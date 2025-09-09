# Advanced Python Concepts

Welcome!  
This repository is dedicated to exploring advanced concepts in Python programming.  
Each section introduces a new topic, explains its significance, and provides practical code examples to help you master Python at a deeper level.

## Index

1. [Metaclasses](#1-metaclasses)
2. [Abstract Base Classes](#2-abstract-base-classes)
3. [Dataclasses](#3-dataclasses)
4. More topics coming soon...

---

## 1. Metaclasses

**What are Metaclasses?**  
Metaclasses allow you to control the creation and behavior of classes themselves.  
They are used for advanced patterns such as enforcing singletons, automatic attribute creation, auto-registering subclasses, or debugging class creation.

**What we've covered in code:**

- **Dynamic Class Creation:**  
  Using the built-in `type` metaclass to create classes dynamically.  
  *See: [`MetaClasses/basics.py`](MetaClasses/basics.py)*

- **Singleton Pattern with Metaclass:**  
  Implementing a custom metaclass to ensure only one instance of a class exists (singleton).  
  *See: [`MetaClasses/custom_metaclasses.py`](MetaClasses/custom_metaclasses.py)*

- **Function-based Metaclass:**  
  Using a function as a metaclass to intercept and debug class creation.  
  *See: [`MetaClasses/custom_metaclasses.py`](MetaClasses/custom_metaclasses.py)*

- **Enforcing Coding Standards with Metaclass:**  
  Creating a custom metaclass to enforce naming conventions for class attributes and methods (e.g., constants in UPPER_CASE, methods in snake_case).  
  *See: [`MetaClasses/coding_standards.py`](MetaClasses/coding_standards.py)*

- **Auto-registering Subclasses with Metaclass:**  
  Using a metaclass to automatically register subclasses in a registry for easy lookup and management.  
  *See: [`MetaClasses/auto_registering.py`](MetaClasses/auto_registering.py)*

#### When to Use Metaclasses in Real Projects

**✅ Good Use Cases**
- Framework Development: Creating ORMs, web frameworks, or API libraries where you need to control class creation extensively
- Design Pattern Enforcement: Implementing singletons, registries, or ensuring specific patterns
- Code Generation: Automatically generating methods, properties, or attributes based on class definition
- Validation: Enforcing coding standards or architectural constraints across many classes
- Plugin Systems: Auto-registration and discovery mechanisms

**❌ Avoid Metaclasses When**
- Simple Modifications: Class decorators are sufficient
- One-off Solutions: The complexity isn't justified for single-use cases
- Team Unfamiliarity: When team members aren't comfortable with metaclass concepts
- Debugging Concerns: When the added complexity makes debugging too difficult

**Summary**  
Metaclasses are a powerful but complex feature in Python. They provide ultimate control over class creation but should be used judiciously.  
*"Metaclasses are deeper magic than 99% of users should ever worry about."* — Tim Peters

---

## 2. Abstract Base Classes

**What are Abstract Base Classes (ABCs)?**  
ABCs are a way to define interfaces in Python. They allow you to specify methods that must be implemented by subclasses, ensuring a consistent API and enforcing design contracts.

**What we've covered in code:**

- **Defining Abstract Base Classes:**  
  Using the `abc` module to create abstract classes with required methods.  
  *See: [`AbstractBaseClasses/basics.py`](AbstractBaseClasses/basics.py)*

- **Implementing Concrete Subclasses:**  
  Creating subclasses that implement all abstract methods.

- **Template Method Pattern:**  
  Using ABCs to define a template method that relies on abstract methods for specific steps.

- **Usage Example:**  
  Demonstrating polymorphism by operating on different vehicle types (Car, Bicycle) through a common interface.

- **Abstract Properties:**  
  Using abstract properties and property setters to enforce that subclasses provide specific attributes and their validation logic.  
  *See: [`AbstractBaseClasses/abstract_properties.py`](AbstractBaseClasses/abstract_properties.py)*

- **Resolving Duck Typing with ABCs:**  
  Using abstract base classes to formally define interfaces (e.g., `Flyable`, `Swimmable`) and ensure objects meet expected behaviors, rather than relying on implicit duck typing.  
  *See: [`AbstractBaseClasses/resolve_duck_typing.py`](AbstractBaseClasses/resolve_duck_typing.py)*

- **Plugin Architecture with ABCs:**  
  Designing a plugin system using abstract base classes to enforce a consistent interface for plugins (e.g., `name`, `version`, `initialize`, `execute`, `cleanup`).  
  Demonstrates plugin registration, management, and usage.  
  *See: [`AbstractBaseClasses/plugin_architecture.py`](AbstractBaseClasses/plugin_architecture.py)*

- **Data Processing Pipeline with ABCs:**  
  Demonstrates how to use abstract base classes to build a flexible data processing pipeline.  
  Each processor (e.g., `TextProcessor`, `NumberProcessor`, `ListProcessor`) inherits from a common abstract base and implements its own validation and processing logic.  
  The pipeline automatically selects the appropriate processor for each data item, ensuring type safety and extensibility.  
  *See: [`AbstractBaseClasses/data_processing_pipeline.py`](AbstractBaseClasses/data_processing_pipeline.py)*

#### When to Use ABCs in Real Projects

**✅ Use ABCs When:**
- Framework Development: Building libraries or frameworks where you need to define clear contracts
- Plugin Systems: When multiple developers need to implement the same interface
- Template Method Pattern: When you have algorithms with varying steps
- Team Development: Large teams need clear specifications
- API Design: Defining consistent interfaces for external consumption
- Polymorphism: When you need to treat different objects uniformly

**❌ Avoid ABCs When:**
- Simple Scripts: Overkill for small, straightforward programs
- Duck Typing Suffices: When the informal protocol is clear and stable
- Single Implementation: When you're only going to have one implementation
- Rapid Prototyping: When flexibility is more important than structure
- Python's Built-in Protocols: When existing protocols (like `__len__`, `__iter__`) are sufficient

**Summary**  
ABCs help enforce consistent interfaces and design contracts, making codebases more maintainable and robust.  
Use them when structure and clarity are important, but avoid unnecessary complexity for simple or rapidly evolving code.

---

## 3. Dataclasses

**What are Dataclasses?**  
Dataclasses, introduced in Python 3.7, provide a decorator and functions for automatically adding special methods to user-defined classes. They simplify the creation of classes that primarily store data, reducing boilerplate code for methods like `__init__`, `__repr__`, `__eq__`, and `__hash__`.

**What we've covered in code:**

- **Traditional Data Class Implementation:**  
  Demonstrates how to manually implement a data-holding class with custom `__init__`, `__repr__`, `__eq__`, and `__hash__` methods.  
  *See: [`DataClasses/traditional.py`](DataClasses/traditional.py)*

- **Dataclass-based Implementation:**  
  Shows how to use the `@dataclass` decorator to automatically generate these methods, making code more concise and readable.  
  *See: [`DataClasses/dataclass_solution.py`](DataClasses/dataclass_solution.py)*

- **Dataclass Parameters and Customization:**  
  Explores all the parameters available in the `@dataclass` decorator, such as:
  - `init`: Controls generation of `__init__`
  - `repr`: Controls generation of `__repr__`
  - `eq`: Controls generation of `__eq__`
  - `order`: Enables comparison operators
  - `frozen`: Makes instances immutable
  - `unsafe_hash`: Controls hash generation
  - `slots`: Enables memory-efficient storage
  - `kw_only`, `match_args`, `weakref_slot`: Advanced features for keyword-only fields, pattern matching, and weak references  
  Demonstrates how each parameter affects the generated class, including immutability, ordering, hashability, and memory usage.  
  *See: [`DataClasses/dataclass_parameters.py`](DataClasses/dataclass_parameters.py)*

- **Hashability and Equality:**  
  Explains why implementing both `__eq__` and `__hash__` is important for using custom objects in sets and as dictionary keys.

- **Slots for Memory Management:**  
  Shows how using `slots=True` in dataclasses can reduce memory usage and restrict dynamic attribute creation.  
  *See: [`DataClasses/slots_parameter_memory_mngmt.py`](DataClasses/slots_parameter_memory_mngmt.py)*

  This example demonstrates:
  - How Python objects are represented in memory using `ctypes`.
  - How reference counting works in CPython and its impact on garbage collection.
  - The effect of `sys.getrefcount()` and why some objects (like small integers) are "immortal" in Python 3.11+.
  - How to measure the true memory footprint of Python objects and containers using `sys.getsizeof()` and `pympler.asizeof`.
  - Why `__slots__` can make objects more memory-efficient by removing the per-instance `__dict__`.

---

More advanced Python concepts will be added soon.  
Feel free to explore, modify, and experiment with the code as you deepen your understanding of Python!

---
**Note:** This repository is for educational and personal learning