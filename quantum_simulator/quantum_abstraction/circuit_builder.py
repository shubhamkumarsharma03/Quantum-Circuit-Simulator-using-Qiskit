from typing import List
from .qubit import Qubit
from .gates import (
    Gate, HadamardGate, PauliXGate, PauliYGate, PauliZGate, CNOTGate,
    TGate, PhaseGate, RXGate, RYGate, RZGate, SwapGate
)

class QuantumCircuit:
    """
    Logical representation of a Quantum Circuit.
    Holds a collection of qubits and a sequence of gates applied to them.
    This class is backend-agnostic.
    """
    def __init__(self, num_qubits: int):
        self.qubits = [Qubit(i) for i in range(num_qubits)]
        self.gates: List[Gate] = []
        self.measurements: List[int] = [] # List of qubit indices to measure

    def h(self, qubit_index: int):
        self.gates.append(HadamardGate(self.qubits[qubit_index]))
        return self

    def x(self, qubit_index: int):
        self.gates.append(PauliXGate(self.qubits[qubit_index]))
        return self

    def y(self, qubit_index: int):
        self.gates.append(PauliYGate(self.qubits[qubit_index]))
        return self

    def z(self, qubit_index: int):
        self.gates.append(PauliZGate(self.qubits[qubit_index]))
        return self
    
    def t(self, qubit_index: int):
        self.gates.append(TGate(self.qubits[qubit_index]))
        return self

    def s(self, qubit_index: int):
        self.gates.append(PhaseGate(self.qubits[qubit_index]))
        return self

    def rx(self, qubit_index: int, theta: float):
        self.gates.append(RXGate(self.qubits[qubit_index], theta))
        return self

    def ry(self, qubit_index: int, theta: float):
        self.gates.append(RYGate(self.qubits[qubit_index], theta))
        return self

    def rz(self, qubit_index: int, theta: float):
        self.gates.append(RZGate(self.qubits[qubit_index], theta))
        return self

    def cx(self, control_index: int, target_index: int):
        self.gates.append(CNOTGate(self.qubits[control_index], self.qubits[target_index]))
        return self
    
    def swap(self, idx1: int, idx2: int):
        self.gates.append(SwapGate(self.qubits[idx1], self.qubits[idx2]))
        return self

    def measure_all(self):
        self.measurements = [q.index for q in self.qubits]
        return self

    def measure(self, qubit_indices: List[int]):
        self.measurements.extend(qubit_indices)
        return self

    def __repr__(self) -> str:
        return f"QuantumCircuit(qubits={len(self.qubits)}, gates={len(self.gates)})"
