# DataProcessing

A modular Python library demonstrating advanced concepts such as Abstract Base Classes (ABC), dataclasses, metaclasses, custom exceptions, and logging for robust data processing workflows.

---

## Features

- **Abstract Base Classes:**  
  Enforces a standard interface for all data processors via `DataProcessor`.
- **Metaclass Enforcement:**  
  `ProcessorMeta` ensures all processors follow naming and implementation rules.
- **Dataclasses:**  
  Used for configuration (`ProcessorConfig`) and results (`ProcessingResult`) with type safety and reduced boilerplate.
- **Custom Exceptions:**  
  Clear error handling for validation, processing, and configuration errors.
- **Structured Logging:**  
  Console and rotating file logging for traceability.

---

## Project Structure

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
└── tests/                   # (Add your tests here)
```

---

## Usage Example

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

---

## How It Works

- **Create a ProcessorConfig**  
  Configure limits, validation, and logging.
- **Instantiate a Processor**  
  Use a concrete processor like `NumericProcessor`.
- **Process Data**  
  Call `.process(data)` to get a structured result.
- **Logging**  
  All actions are logged to console and `dataproc.log`.

---

## Extending

To add new processors:
1. Subclass `DataProcessor`.
2. Implement the `process` method.
3. Set a `PROCESSOR_TYPE` class attribute.
4. Ensure your class name ends with `Processor`.

Metaclass rules will enforce these requirements.

---

## Advanced Concepts Demonstrated

- **ABC:** Forces all processors to implement required methods.
- **Metaclass:** Validates processor class structure at creation.
- **Dataclass:** Simplifies config/result objects and enforces type hints.
- **Custom Exceptions:** Improves error clarity and handling.
- **Logging:** Tracks processor lifecycle and results.

---

## Requirements

- Python 3.7+
- No external dependencies required for core functionality.

---

## License

For educational and personal learning