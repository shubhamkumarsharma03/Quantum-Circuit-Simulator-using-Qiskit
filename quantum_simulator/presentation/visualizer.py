import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from ..infrastructure.logger import setup_logger

logger = setup_logger("visualizer")

class QuantumVisualizer:
    """
    Handles ASCII and Graphical visualizations for circuits and results.
    """
    
    @staticmethod
    def print_circuit_ascii(qiskit_circ):
        """
        Prints the circuit in ASCII format to the console.
        """
        print("\n--- Quantum Circuit (ASCII) ---")
        print(qiskit_circ.draw(output='text'))
        print("-------------------------------\n")

    @staticmethod
    def show_circuit_diagram(qiskit_circ):
        """
        Returns the circuit diagram figure.
        """
        print("Generating circuit diagram...")
        # style={'backgroundcolor': '#ffffff'} ensures white background for embedding
        return qiskit_circ.draw(output='mpl')

    @staticmethod
    def plot_results(counts):
        """
        Returns the histogram figure of the measurement results.
        """
        logger.info("Plotting measurement counts...")
        # sort counts ensuring same order
        # plot_histogram returns a matplotlib Figure
        fig = plot_histogram(counts)
        fig.suptitle("Quantum Measurement Results") # Set title on figure
        return fig

    @staticmethod
    def print_results_table(counts):
        """
        Prints a formatted table of results and probabilities.
        """
        total_shots = sum(counts.values())
        print("\n--- Measurement Outcomes ---")
        print(f"{'State':<10} | {'Counts':<10} | {'Probability':<12}")
        print("-" * 38)
        for state, count in sorted(counts.items()):
            prob = count / total_shots
            print(f"{state:<10} | {count:<10} | {prob:<12.4f}")
        print("-" * 38 + "\n")
