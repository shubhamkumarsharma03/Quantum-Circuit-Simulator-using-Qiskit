from ..infrastructure.logger import infra_logger

class CircuitValidator:
    """
    Validates circuit parameters and operations.
    """
    @staticmethod
    def validate_qubit_count(count: int, max_qubits: int):
        if count <= 0:
            raise ValueError("Qubit count must be positive.")
        if count > max_qubits:
            raise ValueError(f"Qubit count exceeds hardware limit of {max_qubits}.")

    @staticmethod
    def validate_gate_targets(qubit_indices: list, total_qubits: int):
        for idx in qubit_indices:
            if idx < 0 or idx >= total_qubits:
                raise IndexError(f"Qubit index {idx} is out of range for circuit size {total_qubits}.")
