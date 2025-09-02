# Advanced Python Concepts

Welcome!  
This repository is dedicated to exploring advanced concepts in Python programming.  
Each section will introduce a new topic, explain its significance, and provide practical code examples to help you master Python at a deeper level.

## Concepts Covered

### 1. Metaclasses

**What are Metaclasses?**  
Metaclasses are a powerful feature in Python that allow you to control the creation and behavior of classes themselves.  
While classes define how instances (objects) behave, metaclasses define how classes behave.  
They are most commonly used for advanced patterns such as enforcing singletons, automatic attribute creation, auto-registering subclasses, or debugging class creation.

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

---

More advanced Python concepts will be added soon.  
Feel free to explore, modify, and experiment with the code as you deepen your understanding of Python!

---
**Note:** This repository is for educational and personal learning purposes.