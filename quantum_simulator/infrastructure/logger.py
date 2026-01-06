import logging
import sys
import os

def setup_logger(name: str = "quantum_simulator", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a production-grade logger with console output.
    
    Args:
        name: The name of the logger.
        level: Logging level (e.g., logging.DEBUG, logging.INFO).
        
    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        
        # Create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        ch.setFormatter(formatter)
        
        # Add the handlers to the logger
        logger.addHandler(ch)
        
    return logger

# Global logger instance for the infrastructure layer
infra_logger = setup_logger("infrastructure")
