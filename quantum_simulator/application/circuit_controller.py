from ..quantum_abstraction.circuit_builder import QuantumCircuit
from ..application.simulation_manager import SimulationManager
from ..application.validators import CircuitValidator
from ..infrastructure.config import load_config
from ..infrastructure.logger import setup_logger

logger = setup_logger("circuit_controller")

class CircuitController:
    """
    Main controller class for the Quantum Simulator application.
    Acts as a Facade for the underlying layers.
    """
    def __init__(self):
        self._config = load_config()
        self._simulation_manager = SimulationManager(self._config.DEFAULT_BACKEND)
        self.current_circuit = None

    def create_circuit(self, num_qubits: int):
        """
        Initializes a new quantum circuit.
        """
        CircuitValidator.validate_qubit_count(num_qubits, self._config.MAX_QUBITS)
        self.current_circuit = QuantumCircuit(num_qubits)
        logger.info(f"New circuit created with {num_qubits} qubits.")
        return self.current_circuit

    def create_bell_state(self):
        """
        Creates a Bell State |Φ+> = (|00> + |11>)/sqrt(2)
        """
        self.create_circuit(2)
        self.current_circuit.h(0)
        self.current_circuit.cx(0, 1)
        logger.info("Created Bell State circuit.")
        return self.current_circuit

    def create_ghz_state(self, n_qubits=3):
        """
        Creates a GHZ State (|0...0> + |1...1>)/sqrt(2)
        """
        self.create_circuit(n_qubits)
        self.current_circuit.h(0)
        for i in range(n_qubits - 1):
            self.current_circuit.cx(i, i+1)
        logger.info(f"Created GHZ State circuit with {n_qubits} qubits.")
        return self.current_circuit

    def create_teleportation_circuit(self):
        """
        Creates a Quantum Teleportation circuit.
        Qubit 0: State to teleport (psi)
        Qubit 1: Alice's half of Bell pair
        Qubit 2: Bob's half of Bell pair
        """
        self.create_circuit(3)
        # 1. Create Bell Pair between Q1 and Q2
        self.current_circuit.h(1)
        self.current_circuit.cx(1, 2)
        
        # 2. Prepare some state to teleport on Q0 (e.g., Rx(pi/3))
        # self.current_circuit.rx(0, 1.047) # User can manually prep Q0
        
        # 3. Bell Measurement on Q0 and Q1
        self.current_circuit.cx(0, 1)
        self.current_circuit.h(0)
        
        # 4. Conditional Operations (Classically controlled not truly possible effectively in this simple sim
        # but we can simulate the circuit logic)
        # Note: In a real teleportation, we measure Q0, Q1 then apply gates.
        # Here we just show the full coherent circuit which is equivalent via deferred measurement principle.
        self.current_circuit.cx(1, 2)
        self.current_circuit.cz(0, 2) # Example: need CZ or H-CX-H logic for CZ
        # Since we don't have CZ, we use H-CX-H on target for Z-control
        # CZ(0, 2) = H(2) CX(0, 2) H(2)
        self.current_circuit.h(2)
        self.current_circuit.cx(0, 2)
        self.current_circuit.h(2)
        
        logger.info("Created Teleportation circuit.")
        return self.current_circuit

    def run_simulation(self, shots: int = None):
        """
        Runs the simulation on the current circuit.
        """
        if not self.current_circuit:
            raise ValueError("No circuit defined. Create a circuit first.")
        
        shots = shots or self._config.DEFAULT_SHOTS
        counts, qiskit_circ = self._simulation_manager.run_simulation(self.current_circuit, shots)
        return counts, qiskit_circ

    def get_classical_comparison(self, bit_index: int, value: int):
        """
        Returns a classical bit simulation result for comparison.
        """
        from ..classical_comparison.classical_bits import ClassicalBitSimulator
        sim = ClassicalBitSimulator(bit_index + 1)
        sim.set_bit(bit_index, value)
        return sim.simulate_stochastic()
