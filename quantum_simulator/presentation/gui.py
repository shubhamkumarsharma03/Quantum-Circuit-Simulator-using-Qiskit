import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ..application.circuit_controller import CircuitController
from .visualizer import QuantumVisualizer

class QuantumGUI:
    """
    Graphical User Interface for the Quantum Simulator using Tkinter.
    Provides a visual way to build circuits and view results.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Industry-Grade Quantum Simulator")
        self.root.geometry("1200x700")
        
        self.controller = CircuitController()
        self.setup_ui()

    def setup_ui(self):
        # Main Layout: PanedWindow
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left Frame: Controls
        self.left_frame = ttk.Frame(self.paned_window, width=400)
        self.paned_window.add(self.left_frame)

        # Right Frame: Visualizations
        self.right_frame = ttk.Frame(self.paned_window, width=800)
        self.paned_window.add(self.right_frame)
        
        # --- Left Frame Content ---
        # Header
        header = ttk.Label(self.left_frame, text="Quantum Circuit Simulator", font=("Helvetica", 14, "bold"))
        header.pack(pady=10)

        # Circuit Init Frame
        init_frame = ttk.LabelFrame(self.left_frame, text="Initialization")
        init_frame.pack(padx=10, pady=5, fill="x")
        
        ttk.Label(init_frame, text="Qubits:").grid(row=0, column=0, padx=5, pady=5)
        self.qubit_entry = ttk.Entry(init_frame, width=5)
        self.qubit_entry.insert(0, "2")
        self.qubit_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(init_frame, text="Create", command=self.create_circuit).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(init_frame, text="Preset:").grid(row=0, column=3, padx=5, pady=5)
        self.algo_choice = tk.StringVar()
        self.algo_combo = ttk.Combobox(init_frame, textvariable=self.algo_choice, values=["Bell State", "GHZ State", "Teleportation"], state="readonly", width=12)
        self.algo_combo.grid(row=0, column=4, padx=5, pady=5)
        self.algo_combo.set("Bell State")
        
        ttk.Button(init_frame, text="Load", command=self.load_algorithm).grid(row=0, column=5, padx=5, pady=5)

        # Operations Frame
        self.ops_frame = ttk.LabelFrame(self.left_frame, text="Operations (Gates)")
        self.ops_frame.pack(padx=10, pady=5, fill="x")
        
        self.setup_gate_controls()
        
        # Disable initially until circuit created
        self.toggle_frame_state(self.ops_frame, "disabled")
        
        # Execution Frame
        exec_frame = ttk.Frame(self.left_frame)
        exec_frame.pack(pady=10)
        
        ttk.Button(exec_frame, text="Run Simulation", command=self.run_sim).pack(side="left", padx=10)
        ttk.Button(exec_frame, text="Visualize Circuit", command=self.visualize_circ).pack(side="left", padx=10)

        # --- Right Frame Content ---
        # Top: Circuit Diagram
        self.plot_frame_top = ttk.LabelFrame(self.right_frame, text="Circuit Diagram")
        self.plot_frame_top.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bottom: Results Histogram
        self.plot_frame_bottom = ttk.LabelFrame(self.right_frame, text="Results Histogram")
        self.plot_frame_bottom.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_gate_controls(self):
        """Helper to organize gate controls in ops_frame"""
        self.gate_choice = tk.StringVar(value="H")
        gates = ["H", "X", "Y", "Z", "S", "T", "RX", "RY", "RZ", "CX", "SWAP"]
        
        # Grid layout for gates
        for i, gate in enumerate(gates):
            row = 0 if i < 6 else 1
            col = i if i < 6 else i - 6
            ttk.Radiobutton(self.ops_frame, text=gate, variable=self.gate_choice, value=gate, command=self.on_gate_select).grid(row=row, column=col, padx=4, pady=2, sticky="w")

        # Control/Target Indices
        self.param_frame = ttk.Frame(self.ops_frame)
        self.param_frame.grid(row=2, column=0, columnspan=6, pady=10)

        ttk.Label(self.param_frame, text="Idx 1:").grid(row=0, column=0, padx=2)
        self.idx1_entry = ttk.Entry(self.param_frame, width=4)
        self.idx1_entry.grid(row=0, column=1, padx=2)
        
        ttk.Label(self.param_frame, text="Idx 2:").grid(row=0, column=2, padx=2)
        self.idx2_entry = ttk.Entry(self.param_frame, width=4)
        self.idx2_entry.grid(row=0, column=3, padx=2)

        ttk.Label(self.param_frame, text="Theta:").grid(row=0, column=4, padx=2)
        self.theta_entry = ttk.Entry(self.param_frame, width=4)
        self.theta_entry.grid(row=0, column=5, padx=2)
        self.theta_entry.insert(0, "3.14")
        
        ttk.Button(self.ops_frame, text="Add Gate", command=self.add_gate).grid(row=3, column=0, columnspan=6, pady=5)
        
        self.on_gate_select()

    def on_gate_select(self):
        gate = self.gate_choice.get()
        # Enable/Disable Theta
        if gate in ["RX", "RY", "RZ"]:
            self.theta_entry.config(state="normal")
        else:
            self.theta_entry.config(state="disabled")
            
        # Enable/Disable Idx 2
        if gate in ["CX", "SWAP"]:
            self.idx2_entry.config(state="normal")
        else:
            self.idx2_entry.config(state="disabled")

    def create_circuit(self):
        try:
            n = int(self.qubit_entry.get())
            self.controller.create_circuit(n)
            self.toggle_frame_state(self.ops_frame, "normal")
            messagebox.showinfo("Success", f"Circuit with {n} qubits created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def load_algorithm(self):
        try:
            algo = self.algo_choice.get()
            if algo == "Bell State":
                self.controller.create_bell_state()
            elif algo == "GHZ State":
                self.controller.create_ghz_state()
            elif algo == "Teleportation":
                self.controller.create_teleportation_circuit()
            
            # Update qubit entry
            n = len(self.controller.current_circuit.qubits)
            self.qubit_entry.delete(0, tk.END)
            self.qubit_entry.insert(0, str(n))
            
            self.toggle_frame_state(self.ops_frame, "normal")
            messagebox.showinfo("Success", f"Loaded {algo} (Qubits: {n})")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_frame_state(self, frame, state):
        for child in frame.winfo_children():
            # Recursively handle sub-frames if needed
            try:
                child.configure(state=state)
            except tk.TclError:
                pass
            # Special case: re-apply logic if enabling
            if state == "normal":
                self.on_gate_select()
            
    def add_gate(self):
        try:
            gate = self.gate_choice.get()
            idx1 = int(self.idx1_entry.get())
            
            if gate == "H": self.controller.current_circuit.h(idx1)
            elif gate == "X": self.controller.current_circuit.x(idx1)
            elif gate == "Y": self.controller.current_circuit.y(idx1)
            elif gate == "Z": self.controller.current_circuit.z(idx1)
            elif gate == "S": self.controller.current_circuit.s(idx1)
            elif gate == "T": self.controller.current_circuit.t(idx1)
            elif gate == "RX": 
                theta = float(self.theta_entry.get())
                self.controller.current_circuit.rx(idx1, theta)
            elif gate == "RY": 
                theta = float(self.theta_entry.get())
                self.controller.current_circuit.ry(idx1, theta)
            elif gate == "RZ": 
                theta = float(self.theta_entry.get())
                self.controller.current_circuit.rz(idx1, theta)
            elif gate == "CX":
                idx2 = int(self.idx2_entry.get())
                self.controller.current_circuit.cx(idx1, idx2)
            elif gate == "SWAP":
                idx2 = int(self.idx2_entry.get())
                self.controller.current_circuit.swap(idx1, idx2)
            
            print(f"Added {gate} gate.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def embed_figure(self, fig, container_frame):
        """Helper to embed a matplotlib figure into a Tkinter frame"""
        # Clear previous plots
        for widget in container_frame.winfo_children():
            widget.destroy()
            
        canvas = FigureCanvasTkAgg(fig, master=container_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run_sim(self):
        try:
            self.controller.current_circuit.measure_all()
            counts, _ = self.controller.run_simulation()
            
            # Embed Histogram
            fig = QuantumVisualizer.plot_results(counts)
            self.embed_figure(fig, self.plot_frame_bottom)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_circ(self):
        try:
            _, q_circ = self.controller.run_simulation(shots=1)
            
            # Embed Circuit Diagram
            fig = QuantumVisualizer.show_circuit_diagram(q_circ)
            self.embed_figure(fig, self.plot_frame_top)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def launch_gui():
    root = tk.Tk()
    app = QuantumGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
