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
