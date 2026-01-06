import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """
    Centralized configuration for the Quantum Simulator.
    Uses environment variables for sensitive or environment-specific data.
    """
    IBM_TOKEN: Optional[str] = os.getenv("IBM_QUANTUM_TOKEN")
    DEFAULT_BACKEND: str = os.getenv("QUANTUM_BACKEND", "aer_simulator")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Simulation defaults
    DEFAULT_SHOTS: int = 1024
    MAX_QUBITS: int = 16

def load_config() -> Config:
    """
    Loads and returns the configuration object.
    In a production system, this might load from a .env file or a vault.
    """
    return Config()
