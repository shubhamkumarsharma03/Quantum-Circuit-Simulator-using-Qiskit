from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session
from .logger import infra_logger

class HardwareBackend:
    """
    Handles execution on real IBM Quantum hardware or IBM cloud simulators.
    Requires a valid IBM API token.
    """
    def __init__(self, token: str, backend_name: str = "ibm_brisbane"):
        try:
            self.service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            self.backend = self.service.backend(backend_name)
        except Exception as e:
            infra_logger.error(f"Failed to connect to IBM Quantum: {e}")
            self.backend = None

    def run(self, qiskit_circ, shots: int = 1024):
        """
        Submits a job to IBM Quantum.
        """
        if not self.backend:
            infra_logger.error("No backend available for hardware execution.")
            return None
        
        with Session(service=self.service, backend=self.backend) as session:
            sampler = Sampler(session=session)
            job = sampler.run(qiskit_circ, shots=shots)
            return job.result()
