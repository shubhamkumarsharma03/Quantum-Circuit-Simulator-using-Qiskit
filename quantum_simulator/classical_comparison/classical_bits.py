import random
from typing import Dict, List

class ClassicalBitSimulator:
    """
    Simulates classical deterministic bits for side-by-side comparison.
    Unlike qubits, classical bits are always in state 0 or 1.
    """
    def __init__(self, num_bits: int):
        self.num_bits = num_bits
        self.bits = [0] * num_bits

    def set_bit(self, index: int, value: int):
        if value not in [0, 1]:
            raise ValueError("Classical bits must be 0 or 1.")
        self.bits[index] = value

    def flip_bit(self, index: int):
        self.bits[index] = 1 - self.bits[index]

    def simulate_stochastic(self, shots: int = 1024) -> Dict[str, int]:
        """
        Simulates classical bits with a fixed state, repeated 'shots' times.
        In the classical case, the result is usually deterministic unless 
        external noise/randomness is added.
        """
        state_str = "".join(map(str, reversed(self.bits)))
        return {state_str: shots}

    @staticmethod
    def get_comparison_explanation():
        return (
            "Classical bits are deterministic and exist in one state at a time (0 or 1).\n"
            "Quantum bits (qubits) can exist in superposition, allowing for multiple \n"
            "states to be explored simultaneously until measurement collapses the state."
        )
