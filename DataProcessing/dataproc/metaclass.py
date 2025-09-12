from abc import ABCMeta

from .exceptions import ValidationError
from .logging import logger


class ProcessorMeta(ABCMeta):
    """
    Metaclass that enforces coding rules for data processors.

    Rules enforced:
    1. All concrete classes must implement a 'process' method
    2. All concrete classes must have a 'PROCESSOR_TYPE' class attribute
    3. Class names must end with 'Processor'
    """

    def __new__(mcs, name, bases, attrs):
        logger.debug(f"Creating class {name} with metaclass ProcessorMeta")
        cls = super().__new__(mcs, name, bases, attrs)

        # skip validation for abstract base classes
        if getattr(cls, "__abstractmethods__", None):
            logger.debug(f"Skipping Validation for abstract class {name}")
            return cls

        # Rule 1
        if not callable(getattr(cls, "process", None)):
            raise ValidationError(f"Class {name} must implement 'process' method")

        # Rule 2
        if not hasattr(cls, "PROCESSOR_TYPE"):
            raise ValidationError(
                f"Class {name} must define 'PROCESSOR_TYPE' class attribute"
            )

        # Rule 3
        if not name.endswith("Processor"):
            raise ValidationError(f"Class {name} must end with with 'Processor'")

        logger.debug(f"Validated processor class {name}")
        return cls
