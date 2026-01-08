# Quantum Computing: Theory & Concepts

Welcome to the **Learning Hub** for the Quantum Circuit Simulator! This document is designed to help students and enthusiasts understand the fundamental concepts behind the circuits you are building.

---

## 📚 1. Core Concepts

### 1.1 The Qubit (Quantum Bit)
Unlike a classical bit that can only be `0` or `1`, a qubit can exist in a **superposition** of both states simultaneously.
Mathematically, a qubit state $|\psi\rangle$ is represented as:

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

Where:
- $|\alpha|^2$ is the probability of measuring `0`.
- $|\beta|^2$ is the probability of measuring `1`.
- $|\alpha|^2 + |\beta|^2 = 1$ (Normalization).

### 1.2 Superposition
Superposition is the ability of a quantum system to be in multiple states at once.
- **Classic Analogy**: A coin spinning on a table is in a mix of Heads and Tails until it stops.
- **Quantum Gate**: The **Hadamard (H)** gate is used to create superposition.

### 1.3 Entanglement
Entanglement is a phenomenon where two or more qubits become linked such that the state of one cannot be described independently of the others.
- If you measure one entangled qubit, you immediately know the state of the other, no matter the distance.
- **Creation**: Typically created using an **H gate** followed by a **CNOT gate**.

### 1.4 Measurement
Measuring a quantum system destroys superposition and collapses the state to a definite `0` or `1`. This is why we run simulations multiple times (shots) to approximate the probabilities (the histogram).

---

## 🚪 2. Quantum Gates Guide

Gates are the building blocks of quantum circuits. They change the state of qubits.

### Single Qubit Gates

| Gate | Symbol | Name | Effect | Matrix |
| :--- | :---: | :--- | :--- | :--- |
| **H** | H | Hadamard | Creates Superposition. Maps $\|0\rangle \to \frac{\|0\rangle + \|1\rangle}{\sqrt{2}}$. | $\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$ |
| **X** | X | Pauli-X | **Quantum NOT**. Flips $\|0\rangle \to \|1\rangle$ and $\|1\rangle \to \|0\rangle$. | $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ |
| **Y** | Y | Pauli-Y | Bit and Phase flip. Rotates around Y-axis. | $\begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}$ |
| **Z** | Z | Pauli-Z | Phase flip. Changes phase of $\|1\rangle$ by $\pi$. | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ |
| **S** | S | Phase Gate | Rotation by $\pi/2$ (90°) around Z-axis. $\sqrt{Z}$. | $\begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix}$ |
| **T** | T | T Gate | Rotation by $\pi/4$ (45°) around Z-axis. $\sqrt[4]{Z}$. | $\begin{bmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{bmatrix}$ |

### Parameterized Gates
These gates take an angle $\theta$ (theta) as a parameter.

- **RX($\theta$)**: Rotate specific degrees around the X axis.
- **RY($\theta$)**: Rotate specific degrees around the Y axis.
- **RZ($\theta$)**: Rotate specific degrees around the Z axis.

### Multi-Qubit Gates

| Gate | Symbol | Name | Description |
| :--- | :---: | :--- | :--- |
| **CNOT** | CX | Controlled-NOT | **Entangler**. Flips the **Target** qubit ONLY if the **Control** qubit is $\|1\rangle$. |
| **SWAP** | --x-- | SWAP | Exchanges the states of two qubits completely. |

---

## 🧩 3. Standard Algorithms Explained

### 3.1 Bell State (Maximal Entanglement)
The simplest example of quantum entanglement.
- **Circuit**: `H(0)` -> `CX(0, 1)`
- **Mechanism**:
    1. `H` puts Qubit 0 into superposition ($|0\rangle + |1\rangle$).
    2. `CX` uses Qubit 0 as a control.
        - If Q0 is 0, Q1 stays 0 -> $|00\rangle$
        - If Q0 is 1, Q1 flips to 1 -> $|11\rangle$
- **Result**: $\frac{|00\rangle + |11\rangle}{\sqrt{2}}$
- **Observation**: You will always measure `00` or `11`. You will never see `01` or `10`.

### 3.2 GHZ State (Multi-Party Entanglement)
Greenberger–Horne–Zeilinger state. Entanglement of 3 or more qubits.
- **Circuit**: `H(0)` -> `CX(0, 1)` -> `CX(0, 2)` ...
- **Result**: $\frac{|000\rangle + |111\rangle}{\sqrt{2}}$
- **Meaning**: All three parties share a unified quantum state.

### 3.3 Quantum Teleportation
A protocol to transfer a quantum state $|\psi\rangle$ from Alice to Bob using entanglement and classical communication.
1. **Entanglement**: Alice and Bob share a Bell pair.
2. **Bell Measurement**: Alice performs a Bell measurement on her qubit ($|\psi\rangle$) and her half of the entangled pair.
3. **Classical Info**: Alice sends 2 classical bits to Bob.
4. **Correction**: Bob applies gates (X or Z) based on the bits to recover $|\psi\rangle$.
*(Note: Matter is not transported, only information!)*

---

## 📈 4. Visualizing Results

### Reading the Histogram
- **X-Axis**: The possible states (e.g., `00`, `01`, `10`, `11`).
- **Y-Axis**: The probability (or frequency) of measuring that state.
- **Interpretation**: In a simulator, we get "perfect" probabilities. On a real quantum computer, noise would introduce small bars for "impossible" states.

### Bloch Sphere (Conceptual)
While not currently visualized in 3D in this app, imagine the qubit state as a point on the surface of a unit sphere.
- **North Pole**: $|0\rangle$
- **South Pole**: $|1\rangle$
- **Equator**: Superposition states like $|+\rangle$ and $|-\rangle$.
- **Rotations**: Gates like X, Y, Z rotate the vector around the respective axes.

---

## 💰 5. Quantum Finance Application

### Angle Encoding
We can map classical data (like stock prices) into quantum states to process them.
- **Technique**: Map a normalized price $p$ to an angle $\theta$.
- **Operation**: Apply $RY(\theta)$ to a qubit.
- **State**: The qubit rotates such that its probability amplitude encodes the price information.
- **Use**: This is the first step for algorithms like Quantum Amplitude Estimation.

---
*Happy Quantizing!*
