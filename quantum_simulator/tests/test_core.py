import pytest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_simulator.quantum_abstraction.circuit_builder import QuantumCircuit
from quantum_simulator.quantum_abstraction.gates import HadamardGate, PauliXGate
from quantum_simulator.execution.qiskit_engine import QiskitEngine

def test_circuit_initialization():
    circ = QuantumCircuit(3)
    assert len(circ.qubits) == 3
    assert len(circ.gates) == 0

def test_gate_addition():
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.x(1)
    assert len(circ.gates) == 2
    assert isinstance(circ.gates[0], HadamardGate)
    assert isinstance(circ.gates[1], PauliXGate)

def test_qiskit_translation():
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    circ.measure_all()
    
    qiskit_circ = QiskitEngine.translate(circ)
    assert qiskit_circ.num_qubits == 2
    # Qiskit circuit usually has data attribute for instructions
    assert len(qiskit_circ.data) >= 3 # H, CX, Measure

def test_bell_state_logic():
    """
    Test that the circuit builder correctly constructs a Bell state (entanglement).
    """
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    # Bell state |Φ+⟩ = 1/√2(|00⟩ + |11⟩)
    assert circ.gates[0].name == "H"
    assert circ.gates[1].name == "CNOT"
    assert circ.gates[1].control.index == 0
    assert circ.gates[1].target.index == 1
