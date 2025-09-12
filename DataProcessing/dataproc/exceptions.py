class DataProcessingError(Exception):
    """Base exception for data processing operations."""

    pass


class ValidationError(DataProcessingError):
    """Raised when data validation fails."""

    pass


class ProcessingError(DataProcessingError):
    """Raised when data processing fails."""

    pass


class ConfigurationError(DataProcessingError):
    """Raised when processor configuration is invalid."""

    pass
