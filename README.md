# Industry-Level Quantum Circuit Simulator Using Qiskit

An educational and scalable quantum circuit simulator built with a professional 5-layer architecture. Designed for students, researchers, and engineers.

## 🌟 New Features
- **Extended Gate Library**: Support for **S, T, RX, RY, RZ, and SWAP** gates.
- **Algorithm Presets**: Built-in generators for **Bell State, GHZ State, and Teleportation**.
- **Enhanced GUI**: Modern split layout with **embedded Matplotlib visualizations** for circuits and results.

## 🏗️ Architecture (5-Layer Model)

1. **Presentation Layer**: CLI (`cli.py`) and Tkinter GUI (`gui.py`) for user interaction.
2. **Application Layer**: Orchestrates the flow using `SimulationManager` and `CircuitController`.
3. **Quantum Abstraction Layer (QAL)**: Backend-agnostic logical models for qubits, gates, and circuits.
4. **Quantum Execution Layer**: High-performance adapters for Qiskit Aer and IBM Quantum hardware.
5. **Infrastructure Layer**: Configuration, logging, and secure IBM authentication.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Pip

### Installation
```bash
pip install -r requirements.txt
```

### Running the Simulator

#### CLI Mode (Default)
```bash
python main.py
```

#### GUI Mode (Recommended)
```bash
python main.py --gui
```

## 🧪 Quantum Concepts Demonstrated

- **Superposition**: Apply the Hadamard (H) gate to enter a probabilistic state.
- **Entanglement**: Create Bell states using H and CNOT gates.
- **Measurement Collapse**: See probabilistic outcomes collapse into deterministic results.
- **Classical Comparison**: Compare quantum behavior with deterministic classical bits.

👉 **[View Examples & Outputs](EXAMPLES.md)** for detailed circuit walkthroughs.

## 📁 Project Structure
```text
quantum_simulator/
├── presentation/         # CLI & GUI (Now with Embedded Plots)
├── application/          # Simulation orchestration & Algorithm Presets
├── quantum_abstraction/   # Domain models (Extended Gates)
├── execution/            # Qiskit & Hardware adapters
├── infrastructure/       # Config & Logger
├── classical_comparison/ # Educational classical simulator
└── tests/                # Layer-wise unit tests
```

## 🛠️ Design Principles
- **SOLID**: Clean, maintainable, and extensible code.
- **Dependency Inversion**: Domain logic is decoupled from the execution engine.
- **Layered Architecture**: Strict boundaries between UI, logic, and infrastructure.

---
*Created for deep-reasoning optimized quantum engineering.*
