from abc import ABC, abstractmethod

class DataProcessor(ABC):
    """Abstract base class for data processing"""

    @abstractmethod
    def process(self, data):
        pass

    @abstractmethod
    def validate(self):
        pass

    def can_process(self, data) -> bool:
        try:
            return self.validate(data)
        except Exception as e:
            print(f"Validation Error in {self.__class__.__name__} as {e}")
            return False
        

class TextProcessor(DataProcessor):
    def process(self, data : str) -> str:
        return data.strip().lower()
    
    def validate(self, data) -> bool:
        return isinstance(data, str)
    

class NumberProcessor(DataProcessor):
    def process(self, data : float) -> float:
        return round(data, 2)
    
    def validate(self, data) -> bool:
        return isinstance(data, (int, float))

class ListProcessor(DataProcessor):

    def process(self, data : list) -> list:
        return sorted(data)
    
    def validate(self, data) -> bool:
        return isinstance(data, list)
    

class ProcessingPipeline:
    def __init__(self):
        self.processors : list[DataProcessor] = []
    
    def addProcessor(self, processor: DataProcessor):
        if not isinstance(processor, DataProcessor):
            raise TypeError("Must be DataProcessor")
        self.processors.append(processor)
    
    def process_item(self, data):
        for processor in self.processors:
            if processor.can_process(data):
                return processor.process(data)
        
        raise ValueError(f"No processor found for datatype :{ type(data)}")
    
    def process_batch(self, items):
        results = []
        for item in items:
            try:
                result = self.process_item(item)
                results.append(result)
            except ValueError as e:
                print(f"Processing Error : {e}")
                results.append(None)
        
        return results

class WrongProcessor:
    pass

pipeline = ProcessingPipeline()
pipeline.addProcessor(NumberProcessor())
pipeline.addProcessor(TextProcessor())
pipeline.addProcessor(ListProcessor())
# pipeline.addProcessor(WrongProcessor())  Must be DataProcessor

test_data = [
    "  HELLO WORLD  ",
    3.14159,
    [3, 1, 4, 1, 5],
    {"invalid": "data"}  # This will fail
]

results = pipeline.process_batch(test_data)
print("Results:", results)