"""Logging configuration utilities."""

import logging
from logging import Logger
from typing import Optional


def configure_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Configure application-wide logging.
    
    Args:
        level: Logging level (INFO, DEBUG, WARNING, ERROR)
        log_file: Optional file path to write logs to disk
    """
    lvl = getattr(logging, level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(level=lvl, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", handlers=handlers)


def get_logger(name: str) -> Logger:
    """Get a logger instance for the given module name.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
