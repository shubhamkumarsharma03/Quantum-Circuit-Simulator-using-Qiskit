from ..execution.qiskit_engine import QiskitEngine
from ..execution.simulator_backend import SimulatorBackend
from ..quantum_abstraction.circuit_builder import QuantumCircuit as LogicalCircuit
from ..infrastructure.logger import setup_logger

logger = setup_logger("simulation_manager")

class SimulationManager:
    """
    Orchestrates the entire simulation process.
    Logical Circuit -> Qiskit Translation -> Execution -> Results.
    """
    def __init__(self, backend_type: str = "aer_simulator"):
        self.simulator = SimulatorBackend(backend_type)
        logger.info(f"Simulation Manager initialized with backend: {backend_type}")

    def run_simulation(self, logical_circuit: LogicalCircuit, shots: int = 1024):
        """
        Coordinates the translation and local execution.
        """
        logger.info(f"Starting simulation with {shots} shots...")
        
        # 1. Translate Logical to Qiskit
        qiskit_circ = QiskitEngine.translate(logical_circuit)
        
        # 2. Run simulation
        counts = self.simulator.run(qiskit_circ, shots=shots)
        
        logger.info("Simulation completed successfully.")
        return counts, qiskit_circ
