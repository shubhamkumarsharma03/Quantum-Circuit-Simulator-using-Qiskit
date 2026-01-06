from abc import ABC, abstractmethod
from typing import List, Tuple
from .qubit import Qubit

class Gate(ABC):
    """
    Base abstraction for a Quantum Gate.
    A gate is a unitary operation applied to one or more qubits.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def targets(self) -> List[Qubit]:
        pass

    def __repr__(self) -> str:
        targets_str = ", ".join([str(q.index) for q in self.targets])
        return f"{self.name}({targets_str})"

class SingleQubitGate(Gate, ABC):
    """
    Abstract class for gates that act on a single qubit.
    """
    def __init__(self, target: Qubit):
        self._target = target

    @property
    def targets(self) -> List[Qubit]:
        return [self._target]

class HadamardGate(SingleQubitGate):
    """
    Hadamard Gate (H): Creates superposition.
    Matrix: 1/√2 * [[1, 1], [1, -1]]
    Effect: Map |0⟩ to (|0⟩ + |1⟩)/√2 and |1⟩ to (|0⟩ - |1⟩)/√2.
    """
    @property
    def name(self) -> str:
        return "H"

class PauliXGate(SingleQubitGate):
    """
    Pauli-X Gate: Quantum NOT gate.
    Matrix: [[0, 1], [1, 0]]
    Effect: Bit flip. Map |0⟩ to |1⟩ and |1⟩ to |0⟩.
    """
    @property
    def name(self) -> str:
        return "X"

class PauliYGate(SingleQubitGate):
    """
    Pauli-Y Gate: Complex rotation.
    Matrix: [[0, -i], [i, 0]]
    Effect: Bit and phase flip.
    """
    @property
    def name(self) -> str:
        return "Y"

class PauliZGate(SingleQubitGate):
    """
    Pauli-Z Gate: Phase flip.
    Matrix: [[1, 0], [0, -1]]
    Effect: Maps |1⟩ to -|1⟩, leaves |0⟩ unchanged.
    """
    @property
    def name(self) -> str:
        return "Z"

class MultiQubitGate(Gate, ABC):
    """
    Abstract class for gates that act on multiple qubits.
    """
    def __init__(self, targets: List[Qubit]):
        self._targets = targets

    @property
    def targets(self) -> List[Qubit]:
        return self._targets

class CNOTGate(MultiQubitGate):
    """
    Controlled-NOT Gate (CX): Creates entanglement.
    Targets: [Control Qubit, Target Qubit]
    Effect: Flips the target qubit if the control qubit is |1⟩.
    """
    def __init__(self, control: Qubit, target: Qubit):
        super().__init__([control, target])
        self.control = control
        self.target = target

    @property
    def name(self) -> str:
        return "CNOT"

class PhaseGate(SingleQubitGate):
    """
    S Gate (Phase Gate): Rotation by PI/2 around Z-axis.
    Matrix: [[1, 0], [0, i]]
    """
    @property
    def name(self) -> str:
        return "S"

class TGate(SingleQubitGate):
    """
    T Gate: Rotation by PI/4 around Z-axis.
    Matrix: [[1, 0], [0, e^(i*pi/4)]]
    """
    @property
    def name(self) -> str:
        return "T"

class RotationGate(SingleQubitGate):
    """
    Abstract class for parameterized rotation gates.
    """
    def __init__(self, target: Qubit, theta: float):
        super().__init__(target)
        self.theta = theta
    
    def __repr__(self) -> str:
         return f"{self.name}({self.targets[0].index}, theta={self.theta:.2f})"

class RXGate(RotationGate):
    """
    RX Gate: Rotation around X-axis by theta.
    """
    @property
    def name(self) -> str:
        return "RX"

class RYGate(RotationGate):
    """
    RY Gate: Rotation around Y-axis by theta.
    """
    @property
    def name(self) -> str:
        return "RY"

class RZGate(RotationGate):
    """
    RZ Gate: Rotation around Z-axis by theta.
    """
    @property
    def name(self) -> str:
        return "RZ"

class SwapGate(MultiQubitGate):
    """
    SWAP Gate: Swaps states of two qubits.
    """
    def __init__(self, qubit1: Qubit, qubit2: Qubit):
        super().__init__([qubit1, qubit2])
        self.q1 = qubit1
        self.q2 = qubit2

    @property
    def name(self) -> str:
        return "SWAP"
