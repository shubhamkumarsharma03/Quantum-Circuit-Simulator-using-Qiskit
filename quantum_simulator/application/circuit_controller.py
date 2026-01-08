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
        
        # Educational Stepping State
        self.step_mode = False
        self.current_step = 0 # Points to the index of the next gate to be applied (0 = start)

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

    def get_circuit_statevector(self):
        """
        Returns the statevector for the current circuit.
        """
        if not self.current_circuit:
            raise ValueError("No circuit defined.")
        if len(self.current_circuit.qubits) > 10:
             # Safety check: Statevector grows exponentially 2^N.
             # 10 qubits = 1024 complex numbers (manageable).
             # 20 qubits = 1M complex numbers (slow for GUI).
             raise ValueError("Statevector visualization disabled for > 10 qubits for performance.")
             
             raise ValueError("Statevector visualization disabled for > 10 qubits for performance.")
             
        # Support Stepping:
        target_circuit = self.get_active_circuit()
        return self._simulation_manager.get_statevector(target_circuit)

    def get_classical_comparison(self, bit_index: int, value: int):
        """
        Returns a classical bit simulation result for comparison.
        """
        from ..classical_comparison.classical_bits import ClassicalBitSimulator
        sim = ClassicalBitSimulator(bit_index + 1)
        sim.set_bit(bit_index, value)
        return sim.simulate_stochastic()

    # ===============================
    # Educational Stepping Logic
    # ===============================
    def toggle_step_mode(self, active: bool):
        self.step_mode = active
        if active and self.current_circuit:
            # If activating, start at the end or beginning? Let's start at beginning.
            self.current_step = 0
            
    def step_forward(self):
        if not self.current_circuit: return
        if self.current_step < len(self.current_circuit.gates):
            self.current_step += 1
            
    def step_backward(self):
        if not self.current_circuit: return
        if self.current_step > 0:
            self.current_step -= 1

    def get_active_circuit(self):
        """
        Returns the circuit to be visualized/simulated.
        If step_mode is True, returns partial circuit up to current_step.
        """
        if not self.current_circuit: return None
        
        if not self.step_mode:
            return self.current_circuit
            
        # Create a partial copy
        # We need a new instance so we don't mutate the original when passing to backend
        # Assuming shallow copy is enough since we just want a subset of gates list
        import copy
        partial = copy.copy(self.current_circuit)
        # Deep copy the list structure typically, but QuantumCircuit init makes new lists
        # Let's just make a new one to be safe and clean
        partial = QuantumCircuit(len(self.current_circuit.qubits))
        partial.gates = self.current_circuit.gates[:self.current_step]
        partial.measurements = self.current_circuit.measurements # Keep measurements? Maybe not for partial?
        # Usually partial steps show coherent state, so measurements might interfere if they are in the middle?
        # For now, let's keep them if they are in the range? 
        # Our logical circuit keeps measurements separate. Let's ignore them for step-viz usually.
        partial.measurements = [] 
        
        return partial
