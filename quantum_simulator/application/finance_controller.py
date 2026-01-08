from ..infrastructure.data_provider import StockDataProvider, StockData
from ..quantum_abstraction.circuit_builder import QuantumCircuit
from ..infrastructure.logger import setup_logger

logger = setup_logger("finance_controller")

class FinanceController:
    """
    Controller for quantum finance applications.
    Bridges stock data with quantum circuit generation.
    """
    
    def __init__(self):
        self.data_provider = StockDataProvider()
        self.current_stock_data: StockData = None
        
    def load_stock_data(self, symbol: str, days: int = 10) -> StockData:
        """
        Load historical stock data for a given symbol.
        
        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            days: Number of days to load
            
        Returns:
            StockData object
        """
        logger.info(f"Loading {days} days of data for {symbol}")
        self.current_stock_data = self.data_provider.fetch_stock_data(symbol, days)
        return self.current_stock_data
    
    def create_angle_encoded_circuit(self, stock_data: StockData = None) -> QuantumCircuit:
        """
        Create a quantum circuit using angle encoding.
        Each price point is encoded as RY(θ) on a separate qubit.
        
        Args:
            stock_data: StockData to encode (uses current if None)
            
        Returns:
            QuantumCircuit with angle-encoded data
        """
        if stock_data is None:
            stock_data = self.current_stock_data
            
        if stock_data is None:
            raise ValueError("No stock data loaded. Call load_stock_data() first.")
        
        # Normalize prices to angles
        angles = stock_data.normalize_to_angles()
        n_qubits = len(angles)
        
        logger.info(f"Creating angle-encoded circuit for {stock_data.symbol} with {n_qubits} qubits")
        
        # Create circuit
        circuit = QuantumCircuit(n_qubits)
        
        # Apply RY gates with normalized angles
        for i, angle in enumerate(angles):
            circuit.ry(i, angle)
            
        logger.info(f"Encoded {len(angles)} price points into quantum circuit")
        return circuit
    
    def create_correlated_circuit(self, stock_data: StockData = None) -> QuantumCircuit:
        """
        Create a circuit with entanglement to represent correlations between days.
        Uses RY encoding + CNOT gates between consecutive qubits.
        
        Args:
            stock_data: StockData to encode
            
        Returns:
            QuantumCircuit with correlations
        """
        if stock_data is None:
            stock_data = self.current_stock_data
            
        if stock_data is None:
            raise ValueError("No stock data loaded.")
        
        angles = stock_data.normalize_to_angles()
        n_qubits = len(angles)
        
        logger.info(f"Creating correlated circuit for {stock_data.symbol}")
        
        circuit = QuantumCircuit(n_qubits)
        
        # Angle encoding
        for i, angle in enumerate(angles):
            circuit.ry(i, angle)
        
        # Add correlations via CNOT gates
        for i in range(n_qubits - 1):
            circuit.cx(i, i + 1)
            
        logger.info(f"Added {n_qubits - 1} correlation gates")
        return circuit
    
    def get_available_stocks(self):
        """Returns list of available stock symbols."""
        return self.data_provider.get_available_stocks()
