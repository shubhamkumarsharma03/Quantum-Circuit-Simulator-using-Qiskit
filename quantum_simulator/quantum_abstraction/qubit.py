from dataclasses import dataclass

@dataclass(frozen=True)
class Qubit:
    """
    Logical representation of a Qubit in the domain model.
    A qubit is identified by its index in a quantum register.
    
    In quantum mechanics, a qubit is a two-state quantum-mechanical system.
    Mathematically, it is represented as a unit vector in a 2D complex Hilbert space.
    |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1.
    """
    index: int

    def __repr__(self) -> str:
        return f"Qubit({self.index})"
