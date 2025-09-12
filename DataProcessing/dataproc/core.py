from abc import ABC, abstractmethod
import statistics
import time
from typing import Any

from .dataclass import ProcessingResult, ProcessorConfig
from .metaclass import ProcessorMeta
from .exceptions import *
from .logging import logger


class DataProcessor(ABC, metaclass=ProcessorMeta):
    """
    Abstract base class for data processors.

    All concrete implementations must implement the process method
    and define a PROCESSOR_TYPE class attribute.
    """

    def __init__(self, config: ProcessorConfig):
        self.config = config
        self.logger = logger
        self.logger.info(f"Initialized {self.__class__.__name__} processor")

    @abstractmethod
    def process(self, data: list[Any]) -> ProcessingResult:
        """
        Process the input data and return results.

        Args:
            data: List of data items to process

        Returns:
            ProcessingResult: The processing results

        Raises:
            ValidationError: If input data is invalid
            ProcessingError: If processing fails
        """
        pass

    def validateInput(self, data: list[Any]) -> None:
        """
        Validate input data before processing.

        Args:
            data: Input data to validate

        Raises:
            ValidationError: If validation fails
        """

        if not isinstance(data, list):
            raise ValidationError("Input data must be list")

        if len(data) == 0:
            raise ValidationError("Input data cannot be empty")

        if len(data) > self.config.max_input_size:
            raise ValidationError(
                f"Input size {len(data)} exceeds maximum {self.config.max_input_size}"
            )

        self.logger.debug(f"Input validation passed for {len(data)} items")

    def log_result(self, result: ProcessingResult) -> None:
        """Log processing result if configured to do so."""
        if self.config.log_results:
            self.logger.info(
                f"Processed {len(result.input_data)} items in "
                f"{result.processing_time:.3f}s using {result.processor_name}"
            )


class NumericProcessor(DataProcessor):
    """
    Processor for numeric data - calculates statistics.
    """

    PROCESSOR_TYPE = "numeric"

    def process(self, data: list[Any]) -> ProcessingResult:
        """Process numeric data to calculate statistics."""
        start_time = time.time()

        try:
            if self.config.validate_input:
                self.validateInput(data)

            numeric_data = []
            for item in data:
                try:
                    numeric_data.append(float(item))
                except (ValueError, TypeError) as e:
                    raise ProcessingError(f"Cannot Convert {item} to numeric: {e}")

            result_data = {
                "count": len(numeric_data),
                "sum": sum(numeric_data),
                "mean": statistics.mean(numeric_data),
                "median": statistics.median(numeric_data),
                "min": min(numeric_data),
                "max": max(numeric_data),
            }

            if len(numeric_data) > 1:
                result_data["std_dev"] = statistics.stdev(numeric_data)

            processing_time = time.time() - start_time

            result = ProcessingResult(
                processor_name=self.__class__.__name__,
                input_data=data,
                output_data=result_data,
                processing_time=processing_time,
                metadata={
                    "data_type": "numeric",
                    "processor_type": self.PROCESSOR_TYPE,
                },
            )

            self.log_result(result)
            return result

        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"Processing failed after {processing_time:.3f}s: {e}")
            raise ProcessingError(f"Numeric processing failed: {e}")
