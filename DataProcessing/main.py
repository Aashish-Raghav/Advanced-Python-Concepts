from dataproc.core import NumericProcessor
from dataproc.dataclass import ProcessorConfig


if __name__ == "__main__":
    numeric_config = ProcessorConfig(
        name="NumericStats",
        description="Calculate Numeric Statistics",
        max_input_size=500
    )

    numeric_processor = NumericProcessor(numeric_config)
    
    numeric_data = [45,10,23,43]
    numeric_result = numeric_processor.process(numeric_data)
    print("Numeric Result:")
    print(numeric_result.to_json())
    print()