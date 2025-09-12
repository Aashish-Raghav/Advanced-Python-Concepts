import logging
import logging.handlers


def get_logger(
    name: str = "dataproc", log_file_path: str = "dataproc.log"
) -> logging.Logger:
    """Create and return a configured logger for the library"""

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(ch_formatter)

    # File Handler
    fh = logging.handlers.RotatingFileHandler(
        log_file_path, maxBytes=1024, backupCount=3
    )
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fh_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


logger = get_logger(__name__)
