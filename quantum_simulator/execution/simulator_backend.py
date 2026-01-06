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
