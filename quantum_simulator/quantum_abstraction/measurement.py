from typing import List
from .qubit import Qubit

class Measurement:
    """
    Represents the measurement of one or more qubits.
    In quantum mechanics, measurement collapses the wavefunction into a basis state.
    """
    def __init__(self, qubits: List[Qubit]):
        self.qubits = qubits

    def __repr__(self) -> str:
        indices = [q.index for q in self.qubits]
        return f"Measurement(qubits={indices})"
