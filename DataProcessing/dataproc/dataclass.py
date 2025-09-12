from datetime import datetime
import json
from typing import Any
from dataclasses import dataclass, field
from .exceptions import ConfigurationError


@dataclass
class ProcessorConfig:
    """Configuration for data processors."""

    name: str
    description: str = ""
    max_input_size: int = 1000
    timeout_seconds: int = 30
    validate_input: bool = True
    log_results: bool = True
    additional_pars: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.max_input_size <= 0:
            raise ConfigurationError("max_input_size must be positive.")
        if self.timeout_seconds <= 0:
            raise ConfigurationError("timeout_seconds must be positive.")


# Dataclasses for structured data
@dataclass
class ProcessingResult:
    """Stores the result of a data processing operation."""

    processor_name: str
    input_data: list[Any]
    output_data: Any
    processing_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for serialization."""
        return {
            "processor_name": self.processor_name,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "processing_time": self.processing_time,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
