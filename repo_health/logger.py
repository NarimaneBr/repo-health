import logging
from rich.logging import RichHandler

def setup_logger(verbose: bool = False):
    """Configure the root logger with rich formatting.
    
    If verbose is True, set level to DEBUG, else WARNING. We default to WARNING 
    when not verbose to not clutter the user's terminal output before the final report.
    """
    level = logging.DEBUG if verbose else logging.WARNING
    
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    
    logger = logging.getLogger("repo_health")
    logger.setLevel(level)
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a child logger."""
    return logging.getLogger(f"repo_health.{name}")
