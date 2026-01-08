from qiskit_aer import Aer
from qiskit import transpile
from typing import Dict

class SimulatorBackend:
    """
    Handles local simulation using Qiskit's Aer simulator.
    """
    def __init__(self, backend_name: str = "aer_simulator"):
        self.backend = Aer.get_backend(backend_name)

    def run(self, qiskit_circ, shots: int = 1024) -> Dict[str, int]:
        """
        Executes the circuit on the local simulator.
        
        Transpilation is the process of rewriting a quantum circuit to match 
        the topology and gate set of a specific quantum device.
        """
        transpiled_circuit = transpile(qiskit_circ, self.backend)
        job = self.backend.run(transpiled_circuit, shots=shots)
        result = job.result()
        return result.get_counts()

    def run_statevector(self, qiskit_circ):
        """
        Runs the circuit on a statevector simulator to get the full quantum state.
        Useful for educational visualizations (Bloch sphere).
        """
        # specialized backend for statevector
        sv_backend = Aer.get_backend('statevector_simulator')
        
        # Remove measurements to get the coherent state
        # (Statevector sim will fail or give collapsed, post-measurement state if measured)
        # We want to see the state BEFORE measurement for education usually.
        # So we create a copy without measurements.
        circ_no_meas = qiskit_circ.copy()
        circ_no_meas.remove_final_measurements() 

        transpiled_circuit = transpile(circ_no_meas, sv_backend)
        job = sv_backend.run(transpiled_circuit)
        result = job.result()
        return result.get_statevector()
