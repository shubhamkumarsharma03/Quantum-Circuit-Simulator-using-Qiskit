
import numpy as np
from ..quantum_abstraction.circuit_builder import QuantumCircuit
from ..execution.qiskit_engine import QiskitEngine
from qiskit.quantum_info import Statevector, state_fidelity

class ChallengeManager:
    """
    Manages educational challenges and verifies user solutions.
    """
    def __init__(self):
        self.challenges = {
            "plus_state": {
                "name": "Superposition Maker",
                "description": "Create the |+> state: (|0> + |1>) / sqrt(2).",
                "qubits": 1,
                "target_circuit": self._make_plus()
            },
            "bell_state": {
                "name": "Bell State Engineer",
                "description": "Create the Bell State |Φ+>: (|00> + |11>) / sqrt(2).",
                "qubits": 2,
                "target_circuit": self._make_bell()
            },
            "ghz_state": {
                "name": "GHZ Creator",
                "description": "Create a 3-qubit GHZ State: (|000> + |111>) / sqrt(2).",
                "qubits": 3,
                "target_circuit": self._make_ghz()
            }
        }
        self.current_challenge_key = None

    def get_challenges(self):
        return [f"{k}: {v['name']}" for k, v in self.challenges.items()]

    def set_challenge(self, key_str):
        # key_str format "key: name"
        key = key_str.split(":")[0]
        if key in self.challenges:
            self.current_challenge_key = key
            return self.challenges[key]
        return None

    def check_solution(self, user_circuit):
        if not self.current_challenge_key:
            return False, "No challenge selected."

        challenge = self.challenges[self.current_challenge_key]
        
        # 1. Check Qubit Count
        if len(user_circuit.qubits) != challenge["qubits"]:
            return False, f"Incorrect qubit count. Expected {challenge['qubits']}."

        # 2. Compute Statevectors
        # We need to use the engine to get statevectors without running full sim mechanism if possible,
        # or use Qiskit directly for verification to ensure accuracy.
        try:
            # User State
            user_qc = QiskitEngine.translate(user_circuit)
            user_sv = Statevector.from_instruction(user_qc)
            
            # Target State
            target_qc = QiskitEngine.translate(challenge["target_circuit"])
            target_sv = Statevector.from_instruction(target_qc)
            
            # 3. Check Fidelity
            fidelity = state_fidelity(user_sv, target_sv)
            
            if fidelity > 0.99:
                return True, f"Success! Fidelity: {fidelity:.4f}"
            else:
                return False, f"Incorrect state. Fidelity: {fidelity:.4f}"
                
        except Exception as e:
            return False, f"Verification Error: {e}"

    # --- Target Generators ---
    def _make_plus(self):
        qc = QuantumCircuit(1)
        qc.h(0)
        return qc

    def _make_bell(self):
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        return qc
        
    def _make_ghz(self):
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(1, 2)
        return qc
