"""
Comprehensive test suite for the data processing library.

This test suite covers:
- Unit tests for all classes and functions
- Integration tests for the complete workflow
- Error handling and edge cases
- Metaclass behavior
- Logging functionality

Run with: python -m unittest tests.test_data_processing -v
"""


from datetime import datetime
import json
import unittest

from dataproc.core import DataProcessor, NumericProcessor
from dataproc.exceptions import ConfigurationError, ProcessingError, ValidationError
from dataproc.dataclass import ProcessingResult, ProcessorConfig
# from dataproc.core import NumericProcessor

class TestData(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = [1, 2, 3, 4, 5]
        self.sample_output = {'mean': 3.0, 'count': 5}
    
    def test_processing_result_creation(self):
        """Test ProcessingResult creation and methods."""

        result = ProcessingResult(
            processor_name="TestProcessor",
            input_data=self.sample_data,
            output_data=self.sample_output,
            processing_time=0.123
        )

        self.assertEqual(result.processor_name, "TestProcessor")
        self.assertEqual(result.input_data, self.sample_data)
        self.assertEqual(result.output_data, self.sample_output)
        self.assertEqual(result.processing_time, 0.123)
        self.assertIsInstance(result.timestamp, datetime)
        self.assertEqual(result.metadata, {})
    
    def test_processing_result_to_dict(self):
        """Test ProcessingResult to_dict method."""
        result = ProcessingResult(
            processor_name="TestProcessor",
            input_data=self.sample_data,
            output_data=self.sample_output,
            processing_time=0.123
        )
        
        result_dict = result.to_dict()
        self.assertIn('processor_name', result_dict)
        self.assertIn('timestamp', result_dict)
        self.assertIsInstance(result_dict['timestamp'], str)
    
    def test_processing_result_to_json(self):
        """Test ProcessingResult to_json method."""
        result = ProcessingResult(
            processor_name="TestProcessor",
            input_data=self.sample_data,
            output_data=self.sample_output,
            processing_time=0.123
        )
        
        json_str = result.to_json()
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed['processor_name'], "TestProcessor")
    
    def test_processor_config_creation(self):
        """Test ProcessorConfig creation."""
        config = ProcessorConfig(
            name="TestConfig",
            description="Test configuration",
            max_input_size=100,
            timeout_seconds=10.0
        )
        
        self.assertEqual(config.name, "TestConfig")
        self.assertEqual(config.description, "Test configuration")
        self.assertEqual(config.max_input_size, 100)
        self.assertEqual(config.timeout_seconds, 10.0)
        self.assertTrue(config.validate_input)
        self.assertTrue(config.log_results)
    
    def test_processor_config_validation(self):
        """Test ProcessorConfig validation in __post_init__."""
        with self.assertRaises(ConfigurationError):
            ProcessorConfig(name="Test", max_input_size=-1)
            
        with self.assertRaises(ConfigurationError):
            ProcessorConfig(name="Test", timeout_seconds=-1.0)


class TestProcessorMeta(unittest.TestCase):
    """Test metaclass behavior."""
    
    def test_metaclass_enforcement_success(self):
        """Test that properly defined classes pass metaclass validation."""
        # This should work fine
        class ValidProcessor(DataProcessor):
            PROCESSOR_TYPE = "valid"
            
            def process(self, data):
                return ProcessingResult(
                    processor_name=self.__class__.__name__,
                    input_data=data,
                    output_data={},
                    processing_time=0.0
                )
        
        # Should be able to create an instance
        config = ProcessorConfig(name="test")
        processor = ValidProcessor(config)
        self.assertIsInstance(processor, ValidProcessor)
    
    def test_metaclass_enforcement_missing_process(self):
        """Test that classes without process method fail validation."""
        with self.assertRaises(ValidationError) as context:
            class InvalidProcessor(DataProcessor):
                PROCESSOR_TYPE = "invalid"
                # Missing process method
        
        self.assertIn("must implement 'process' method", str(context.exception))
        
    def test_metaclass_enforcement_missing_processor_type(self):
        """Test that classes without PROCESSOR_TYPE fail validation."""
        with self.assertRaises(ValidationError) as context:
            class InvalidProcessor(DataProcessor):
                def process(self, data):
                    pass
                # Missing PROCESSOR_TYPE
        
        self.assertIn("must define 'PROCESSOR_TYPE' class attribute", str(context.exception))
        
    def test_metaclass_enforcement_naming_convention(self):
        """Test that classes not ending with 'Processor' fail validation."""
        with self.assertRaises(ValidationError) as context:
            class InvalidHandler(DataProcessor):
                PROCESSOR_TYPE = "invalid"
                
                def process(self, data):
                    pass
        
        self.assertIn("must end with 'Processor'", str(context.exception))


class TestAbstractBaseClass(unittest.TestCase):
    """Test abstract base class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = ProcessorConfig(name="TestProcessor")
        
    def test_cannot_instantiate_abstract_class(self):
        """Test that DataProcessor cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            DataProcessor(self.config)
            
    def test_validate_input_valid_data(self):
        """Test input validation with valid data."""
        processor = NumericProcessor(self.config)
        # Should not raise exception
        processor.validateInput([1, 2, 3])
        
    def test_validate_input_invalid_type(self):
        """Test input validation with invalid type."""
        processor = NumericProcessor(self.config)
        with self.assertRaises(ValidationError):
            processor.validateInput("not a list")
            
    def test_validate_input_empty_data(self):
        """Test input validation with empty data."""
        processor = NumericProcessor(self.config)
        with self.assertRaises(ValidationError):
            processor.validateInput([])
            
    def test_validate_input_too_large(self):
        """Test input validation with data exceeding max size."""
        config = ProcessorConfig(name="Test", max_input_size=3)
        processor = NumericProcessor(config)
        with self.assertRaises(ValidationError):
            processor.validateInput([1, 2, 3, 4, 5])

class TestNumericProcessor(unittest.TestCase):
    """Test NumericProcessor functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = ProcessorConfig(name="NumericTest")
        self.processor = NumericProcessor(self.config)
        
    def test_process_valid_numbers(self):
        """Test processing valid numeric data."""
        data = [1, 2, 3, 4, 5]
        result = self.processor.process(data)
        
        self.assertIsInstance(result, ProcessingResult)
        self.assertEqual(result.processor_name, "NumericProcessor")
        self.assertEqual(result.input_data, data)
        
        output = result.output_data
        self.assertEqual(output['count'], 5)
        self.assertEqual(output['sum'], 15)
        self.assertEqual(output['mean'], 3.0)
        self.assertEqual(output['min'], 1)
        self.assertEqual(output['max'], 5)
        
    def test_process_mixed_convertible_data(self):
        """Test processing data that can be converted to numbers."""
        data = ['1', '2.5', 3, 4.0]
        result = self.processor.process(data)
        
        output = result.output_data
        self.assertEqual(output['count'], 4)
        self.assertEqual(output['sum'], 10.5)
        
    def test_process_invalid_data(self):
        """Test processing data that cannot be converted to numbers."""
        data = [1, 2, 'invalid', 4]
        with self.assertRaises(ProcessingError):
            self.processor.process(data)
            
    def test_process_single_value(self):
        """Test processing single value (no std deviation)."""
        data = [5]
        result = self.processor.process(data)
        
        output = result.output_data
        self.assertEqual(output['count'], 1)
        self.assertNotIn('std_dev', output)  # Should not calculate std_dev for single value
