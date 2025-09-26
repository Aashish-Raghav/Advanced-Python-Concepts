# Advanced Python Concepts

Welcome!  
This repository is dedicated to exploring advanced concepts in Python programming.  
Each section introduces a new topic, explains its significance, and provides practical code examples to help you master Python at a deeper level.

## Index

1. [Metaclasses](#1-metaclasses)
2. [Abstract Base Classes](#2-abstract-base-classes)
3. [Dataclasses](#3-dataclasses)
4. [Data Processing Library Example](#4-data-processing-library-example)
5. [Asyncio](#5-asyncio)
6. [Async Fetcher Library Example](#6-asyncfetcher-asynchronous-http-fetching-library)
7. More topics coming soon...

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

- **Field Function and Default Factories:**  
  Explains why mutable default values (like lists or dicts) should not be used directly in dataclass fields, and how to use `field(default_factory=...)` to safely create new instances for each object.  
  *See: [`DataClasses/field_function.py`](DataClasses/field_function.py)*

  This example demonstrates:
  - The dangers of using mutable defaults in dataclasses (shared state across instances).
  - How `field(default_factory=...)` solves this by creating a new object for each instance.
  - The code generation logic Python uses for dataclass fields with defaults and factories.

- **Advanced Field Parameters:**  
  Shows how to use advanced features of the `field()` function, such as `default_factory`, `repr`, `compare`, and `init`, to customize dataclass behavior.  
  *See: [`DataClasses/field_fxn_parameters.py`](DataClasses/field_fxn_parameters.py)*

  This example demonstrates:
  - Automatically generating unique IDs and timestamps for each instance.
  - Excluding fields from `repr` and comparisons.
  - Creating fields that are initialized in `__post_init__` rather than the constructor.
  - Managing mutable fields like lists and dicts safely.
  - Customizing how fields are displayed and compared.

- **Strict Enforcement of Dataclasses:**  
  Explains how Python's dataclasses do not enforce type hints at runtime by default, and demonstrates several ways to add strict type checking:
  - Using static type checkers (e.g., mypy, pyright, IDE support) for compile-time safety.
  - Adding runtime validation in the `__post_init__` method to check types and raise errors.
  - Leveraging third-party libraries like `pydantic` and `attrs` for automatic validation and type enforcement.
  - Using decorators like `beartype` for runtime enforcement of type hints.
  *See: [`DataClasses/strict_enforcement_dataclasses.py`](DataClasses/strict_enforcement_dataclasses.py)*

  This example demonstrates:
  - The difference between type hints and actual runtime enforcement.
  - How to catch type errors early, both statically and dynamically.
  - How to integrate dataclasses with popular validation libraries for robust data modeling.

---

## 4. Data Processing Library Example

**What is the DataProcessing Library?**  
A modular Python library (see `DataProcessing/`) that demonstrates how advanced Python concepts—metaclasses, abstract base classes, dataclasses, custom exceptions, and logging—can be combined to build robust, extensible, and maintainable data processing workflows.

**Key Features:**

- **Abstract Base Classes:**  
  Enforces a standard interface for all data processors via `DataProcessor`.
- **Metaclass Enforcement:**  
  `ProcessorMeta` ensures all processors follow naming and implementation rules.
- **Dataclasses:**  
  Used for configuration (`ProcessorConfig`) and results (`ProcessingResult`) with type safety and reduced boilerplate.
- **Custom Exceptions:**  
  Clear error handling for validation, processing, and configuration errors.
- **Structured Logging:**  
  Console and file logging for traceability.

**Project Structure:**
```
DataProcessing/
│
├── main.py                  # Example usage script
├── readme.md                # Project documentation
├── dataproc/
│   ├── __init__.py          # Library description
│   ├── core.py              # Core processor classes
│   ├── dataclass.py         # Dataclasses for config/results
│   ├── exceptions.py        # Custom exceptions
│   ├── logging.py           # Logging setup
│   ├── metaclass.py         # Metaclass for enforcement
│   └── __pycache__/         # Compiled Python files
└── tests/
    └── test_data_processing.py  # Comprehensive test suite
```

**Usage Example:**
```python
from dataproc.core import NumericProcessor
from dataproc.dataclass import ProcessorConfig

if __name__ == "__main__":
    numeric_config = ProcessorConfig(
        name="NumericStats",
        description="Calculate Numeric Statistics",
        max_input_size=500
    )

    numeric_processor = NumericProcessor(numeric_config)
    numeric_data = [45, 10, 23, 43]
    numeric_result = numeric_processor.process(numeric_data)
    print("Numeric Result:")
    print(numeric_result.to_json())
```

**Testing:**

A comprehensive test suite is provided in `tests/test_data_processing.py`:

- Unit and integration tests for all classes and workflows
- Error handling and edge cases
- Metaclass and ABC enforcement
- Logging verification

Run all tests with:
```bash
python -m unittest tests.test_data_processing -v
```

**Summary:**  
The DataProcessing library is a practical demonstration of how advanced Python features can be used together to create clean, extensible, and production-ready code. Explore the codebase to see these concepts in action!

---

## 5. Asyncio

**What is Asyncio?**  
Asyncio is Python’s built-in library for asynchronous programming, enabling concurrent code execution using coroutines, tasks, and an event loop. It’s ideal for I/O-bound and high-level structured network code.

**What we've covered in code:**

- **Core Concepts and Basics:**  
  - **Event Loop:** The engine that drives asyncio, running coroutines, scheduling tasks, and handling I/O events.
  - **Coroutine:** Functions defined with `async def` that can be paused and resumed.
  - **Await:** Suspends the coroutine until the awaited object completes.
  - **Task:** A wrapper around a coroutine, scheduled on the event loop and running concurrently.
  - **Future:** A low-level object representing a result not yet available.
  - **Relationship:** Event Loop manages Tasks → Tasks wrap Coroutines → Coroutines use await → await works on awaitables (coroutines, tasks, futures).
  *See: [`Asyncio/basics.py`](Asyncio/basics.py)*

- **Event Loop Usage:**  
  Demonstrates different ways to run coroutines and schedule tasks, including direct execution, task creation, and running multiple tasks concurrently.
  *See: [`Asyncio/event_loop.py`](Asyncio/event_loop.py)*

- **Concurrency Primitives:**  
  Shows how to coordinate and synchronize coroutines using:
  - **Queue:** Producer-consumer patterns and message passing.
  - **Lock:** Ensures mutual exclusion for shared resources.
  - **Event:** Signals and synchronizes between coroutines.
  - **Semaphore:** Limits concurrency, controlling how many coroutines run simultaneously.
  *See: [`Asyncio/concurrency_primitives.py`](Asyncio/concurrency_primitives.py)*

- **Coordination Patterns:**  
  Demonstrates higher-level coordination and control of concurrent tasks:
  - **as_completed:** Process tasks as they finish, regardless of order.
  - **gather:** Run multiple tasks concurrently and collect all results.
  - **wait / wait_for:** Wait for tasks with flexible completion or timeout conditions.
  - **shield:** Protect critical tasks from cancellation by parent coroutines.
  - **timeout:** Handle timeouts for long-running tasks.
  *See: [`Asyncio/coordination_patterns.py`](Asyncio/coordination_patterns.py)*

- **Cancellation Patterns:**  
  Demonstrates best practices for cancelling and cleaning up asyncio tasks:
  - **Basic Cancellation:** How to cancel a running task and handle cleanup using `asyncio.CancelledError`.
  - **Graceful Shutdown:** Using an `Event` to signal workers to stop, allowing for cooperative and clean shutdown before forced cancellation.
  - **Best Practices:** Prefer cooperative shutdown signals over abrupt cancellation; always clean up resources.
  *See: [`Asyncio/cancellation_patterns.py`](Asyncio/cancellation_patterns.py)*

- **Streaming Patterns:**  
  Explores asynchronous iteration and data streaming:
  - **Async Iterator:** Lazily generates values on demand, preserves sequence, and supports stateful logic.
  - **Async Generator:** Streams data using `yield` in an async context, supports multiple consumption patterns (`async for`, `__anext__`, `asend`, comprehensions).
  - **Comparison:** Highlights differences between async iterators/generators and coordination patterns like `as_completed`.
  *See: [`Asyncio/streaming_patterns.py`](Asyncio/streaming_patterns.py)*

- **Task Groups:**  
  Demonstrates structured concurrency in Python 3.11+ using `asyncio.TaskGroup`:
  - **TaskGroup:** Provides a context manager for grouping tasks, ensuring all tasks are managed and cleaned up together.
  - **Exception Handling:** Uses `ExceptionGroup` for fail-fast error propagation and collective exception handling.
  - **Comparison:** Shows differences between `asyncio.gather` (older API) and `TaskGroup` (newer, more structured API).
  - **Best Practices:** Prefer `TaskGroup` for robust, maintainable concurrent code in modern Python.
  *See: [`Asyncio/task_groups.py`](Asyncio/task_groups.py)*

**How to Run Demos:**  
Uncomment the desired demo in any of the files above and run:
```bash
python Asyncio/event_loop.py
python Asyncio/concurrency_primitives.py
python Asyncio/coordination_patterns.py
python Asyncio/cancellation_patterns.py
python Asyncio/streaming_patterns.py
python Asyncio/task_groups.py
```

#### When to Use Asyncio in Real Projects

**✅ Use Asyncio When:**
- Building network servers, clients, or web frameworks
- Handling many simultaneous I/O-bound tasks (HTTP requests, sockets, file operations)
- Creating producer-consumer pipelines or concurrent workflows
- Streaming data or processing events as they arrive
- You need scalable concurrency without threads

**❌ Avoid Asyncio When:**
- Your workload is CPU-bound (use multiprocessing or threading)
- You need true parallelism (asyncio is single-threaded)
- Simpler synchronous code suffices

**Summary**  
Asyncio provides powerful tools for writing concurrent, scalable, and efficient Python code.  
It is best suited for I/O-bound and event-driven applications, and its primitives allow fine-grained control over concurrency, synchronization, streaming, and graceful cancellation.

---
## 6. AsyncFetcher: Asynchronous HTTP Fetching Library

**What is AsyncFetcher?**  
AsyncFetcher is a Python library for high-performance, concurrent HTTP requests using `asyncio` and `aiohttp`. It demonstrates advanced asynchronous programming patterns, resource management, error handling, and structured logging.

**Key Features:**
- Concurrent HTTP requests with `asyncio` and `aiohttp`
- Retry and timeout logic with exponential backoff
- Concurrency control using `asyncio.Semaphore`
- Structured logging and error handling
- Batch fetching with detailed statistics

**Project Structure:**
```
AsyncFetcher/
├── main.py                      # Example usage script
├── fetcher/                     # Core library
└── tests/                       # Test suite
```

For detailed documentation, usage examples, and testing instructions, see the [AsyncFetcher README](AsyncFetcher/readme.md).

**Additional Resources:**
- [Async or AsyncFetcher Artifact](https://claude.ai/public/artifacts/834b6937-c174-4fea-bc50-26191cf38cfb)

---


More advanced Python concepts will be added soon.  
Feel free to explore, modify, and experiment with the code as you deepen your understanding of Python!

---
**Note:** This repository is for educational and personal learning