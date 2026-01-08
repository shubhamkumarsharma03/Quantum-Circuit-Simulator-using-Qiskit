from qiskit import QuantumCircuit as QiskitCircuit
from .simulator_backend import SimulatorBackend
from ..quantum_abstraction.circuit_builder import QuantumCircuit as LogicalCircuit
from ..quantum_abstraction.gates import (
    HadamardGate, PauliXGate, PauliYGate, PauliZGate, CNOTGate,
    TGate, PhaseGate, RXGate, RYGate, RZGate, SwapGate
)

class QiskitEngine:
    """
    Adapter class that translates logical QuantumCircuit objects into
    Qiskit-specific circuit objects and executes them.
    
    This implements the Adapter Pattern to decouple our domain logic from Qiskit.
    """
    
    def __init__(self):
        """Initialize the Qiskit engine."""
        pass

    @staticmethod
    def translate_to_qiskit(logical_circuit: LogicalCircuit) -> QiskitCircuit:
        """
        Translates a logical circuit to a Qiskit circuit without measurement validation.
        Pure translation for visualization purposes.
        """
        # Create circuit with just qubits initially
        num_qubits = len(logical_circuit.qubits)
        # Only add classical bits if there are measurements
        num_clbits = len(logical_circuit.measurements) if logical_circuit.measurements else 0
        
        qiskit_circ = QiskitCircuit(num_qubits, num_clbits)
        
        for gate in logical_circuit.gates:
            if isinstance(gate, HadamardGate):
                qiskit_circ.h(gate.targets[0].index)
            elif isinstance(gate, PauliXGate):
                qiskit_circ.x(gate.targets[0].index)
            elif isinstance(gate, PauliYGate):
                qiskit_circ.y(gate.targets[0].index)
            elif isinstance(gate, PauliZGate):
                qiskit_circ.z(gate.targets[0].index)
            elif isinstance(gate, TGate):
                qiskit_circ.t(gate.targets[0].index)
            elif isinstance(gate, PhaseGate):
                qiskit_circ.s(gate.targets[0].index)
            elif isinstance(gate, RXGate):
                qiskit_circ.rx(gate.theta, gate.targets[0].index)
            elif isinstance(gate, RYGate):
                qiskit_circ.ry(gate.theta, gate.targets[0].index)
            elif isinstance(gate, RZGate):
                qiskit_circ.rz(gate.theta, gate.targets[0].index)
            elif isinstance(gate, CNOTGate):
                qiskit_circ.cx(gate.control.index, gate.target.index)
            elif isinstance(gate, SwapGate):
                qiskit_circ.swap(gate.q1.index, gate.q2.index)
        
        # Add measurements if they exist
        if num_clbits > 0:
            for i, qubit_index in enumerate(logical_circuit.measurements):
                qiskit_circ.measure(qubit_index, i)
            
        return qiskit_circ

    @staticmethod
    def translate(logical_circuit: LogicalCircuit) -> QiskitCircuit:
        """
        Translates a logical circuit to a Qiskit circuit.
        """
        num_qubits = len(logical_circuit.qubits)
        qiskit_circ = QiskitCircuit(num_qubits, len(logical_circuit.measurements))
        
        for gate in logical_circuit.gates:
            if isinstance(gate, HadamardGate):
                qiskit_circ.h(gate.targets[0].index)
            elif isinstance(gate, PauliXGate):
                qiskit_circ.x(gate.targets[0].index)
            elif isinstance(gate, PauliYGate):
                qiskit_circ.y(gate.targets[0].index)
            elif isinstance(gate, PauliZGate):
                qiskit_circ.z(gate.targets[0].index)
            elif isinstance(gate, TGate):
                qiskit_circ.t(gate.targets[0].index)
            elif isinstance(gate, PhaseGate):
                qiskit_circ.s(gate.targets[0].index)
            elif isinstance(gate, RXGate):
                qiskit_circ.rx(gate.theta, gate.targets[0].index)
            elif isinstance(gate, RYGate):
                qiskit_circ.ry(gate.theta, gate.targets[0].index)
            elif isinstance(gate, RZGate):
                qiskit_circ.rz(gate.theta, gate.targets[0].index)
            elif isinstance(gate, CNOTGate):
                qiskit_circ.cx(gate.control.index, gate.target.index)
            elif isinstance(gate, SwapGate):
                qiskit_circ.swap(gate.q1.index, gate.q2.index)
        
        for i, qubit_index in enumerate(logical_circuit.measurements):
            qiskit_circ.measure(qubit_index, i)
            
        return qiskit_circ
