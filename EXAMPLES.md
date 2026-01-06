# Simulator Examples

This document provides example usage for the **Industry-Grade Quantum Simulator**. You can run these examples using the GUI Presets or chemically via the CLI (future implementation). Currently, the best way to explore these is via the `python main.py --gui` interface.

## 1. Bell State (Entanglement)
**Goal**: Create a pair of entangled qubits.
**Mathematical State**: $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$

### Steps:
1. Initialize a circuit with **2 qubits**.
2. Apply **Hadamard (H)** to Qubit 0.
3. Apply **CNOT** (Qubit 0 as Control, Qubit 1 as Target).

### Expected Output:
- **Histogram**: ~50% probability for `00` and ~50% for `11`.
- **Circuit Diagram**:
```
q0: ──H────■────M──
           │    ║
q1: ───────+────M──
```

---

## 2. GHZ State (Multipartite Entanglement)
**Goal**: Entangle three or more qubits.
**Mathematical State**: $|GHZ\rangle = \frac{|000\rangle + |111\rangle}{\sqrt{2}}$

### Steps:
1. Initialize a circuit with **3 qubits**.
2. Apply **H** to Qubit 0.
3. Apply **CNOT** (0 -> 1).
4. Apply **CNOT** (1 -> 2).

### Expected Output:
- **Histogram**: ~50% `000` and ~50% `111`.
- Probabilities for other states (e.g., `001`, `010`) should be near zero (noise-free simulation).

---

## 3. Quantum Teleportation
**Goal**: Transfer the state of one qubit to another using entanglement and classical communication.

### Circuit Logic:
1. **Entanglement**: Create a Bell pair between Alice (Q1) and Bob (Q2).
2. **Preparation**: Prepare the payload state on Alice's Qubit (Q0) (e.g., using RX/RY gates).
3. **Bell Measurement**: Alice performs CNOT(Q0, Q1) and H(Q0), then measures logic.
4. **Correction**: Bob applies X and Z gates based on Alice's results (Simulated via deferred gates here).

### Expected Output:
- If Q0 was prepared in state $|1\rangle$, Bob's qubit (Q2) will be measured as `1` with 100% probability.
- If Q0 was in superposition, Bob's qubit will match the statistics of the original state.

---

## 4. Single Qubit Rotation (Parametric Gates)
**Goal**: Rotate a qubit state by a specific angle $\theta$.

### Steps:
1. Initialize **1 qubit**.
2. Select **RX** (Rotation X) gate.
3. Enter Theta = `3.14` (approx $\pi$).
4. Apply to Qubit 0.

### Expected Output:
- Since $RX(\pi)$ is equivalent to a Pauli-X (NOT) gate:
- **Histogram**: 100% probability of state `1`.
