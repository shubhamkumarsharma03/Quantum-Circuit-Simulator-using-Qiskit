import sys
from ..application.circuit_controller import CircuitController
from .visualizer import QuantumVisualizer

def main_menu():
    controller = CircuitController()
    visualizer = QuantumVisualizer()
    
    print("================================================")
    print("Welcome to the Industry-Grade Quantum Simulator")
    print("================================================")
    
    try:
        n_qubits = int(input("Enter number of qubits for your circuit: "))
        controller.create_circuit(n_qubits)
    except Exception as e:
        print(f"Error: {e}")
        return

    while True:
        print("\n--- Circuit Operations ---")
        print("1. Add Hadamard Gate (H)")
        print("2. Add Pauli-X Gate (X)")
        print("3. Add Pauli-Y Gate (Y)")
        print("4. Add Pauli-Z Gate (Z)")
        print("5. Add CNOT Gate (CX)")
        print("6. Measure All & Run Simulation")
        print("7. Visualize Circuit (Diagram)")
        print("8. Classical Comparison")
        print("0. Exit")
        
        choice = input("\nSelect an option: ")
        
        try:
            if choice == "1":
                idx = int(input("Target qubit index: "))
                controller.current_circuit.h(idx)
            elif choice == "2":
                idx = int(input("Target qubit index: "))
                controller.current_circuit.x(idx)
            elif choice == "3":
                idx = int(input("Target qubit index: "))
                controller.current_circuit.y(idx)
            elif choice == "4":
                idx = int(input("Target qubit index: "))
                controller.current_circuit.z(idx)
            elif choice == "5":
                ctrl = int(input("Control qubit index: "))
                tgt = int(input("Target qubit index: "))
                controller.current_circuit.cx(ctrl, tgt)
            elif choice == "6":
                controller.current_circuit.measure_all()
                counts, q_circ = controller.run_simulation()
                visualizer.print_results_table(counts)
                visualizer.plot_results(counts)
            elif choice == "7":
                _, q_circ = controller.run_simulation(shots=1) # Just to get the qiskit object
                visualizer.print_circuit_ascii(q_circ)
                visualizer.show_circuit_diagram(q_circ)
            elif choice == "8":
                idx = int(input("Bit index: "))
                val = int(input("Initial value (0/1): "))
                results = controller.get_classical_comparison(idx, val)
                print(f"Classical Stochastic Result: {results}")
                from ..classical_comparison.classical_bits import ClassicalBitSimulator
                print(ClassicalBitSimulator.get_comparison_explanation())
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Operation failed: {e}")

if __name__ == "__main__":
    main_menu()
