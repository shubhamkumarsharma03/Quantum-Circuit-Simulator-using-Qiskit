import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import mplcursors
import threading
import time
import webbrowser
import os

from ..application.circuit_controller import CircuitController
from ..application.finance_controller import FinanceController
from ..application.challenge_manager import ChallengeManager
from ..execution.qiskit_engine import QiskitEngine
from .visualizer import QuantumVisualizer

# Set default appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class QuantumGUI(ctk.CTk):
    """
    Modern GUI for the Quantum Simulator using CustomTkinter.
    Features: Dark/Light mode, Threading, Resizable panes, Interactive plots.
    """
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Quantum Circuit Simulator using Qiskit")
        self.geometry("1400x900")
        
        # Controllers
        # Controllers
        self.controller = CircuitController()
        self.finance_controller = FinanceController()
        self.challenge_manager = ChallengeManager()
        
        # State
        self.current_theme = "Dark"
        
        self.setup_ui()

    def setup_ui(self):
        # --- Top Bar ---
        self.top_bar = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.top_bar.pack(side="top", fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(self.top_bar, text="Quantum Simulator", font=("Roboto", 20, "bold"))
        self.title_label.pack(side="left", padx=20, pady=10)
        
        self.theme_switch = ctk.CTkSwitch(self.top_bar, text="Dark Mode", command=self.toggle_theme, onvalue="Dark", offvalue="Light")
        self.theme_switch.select() # Default Dark
        self.theme_switch.pack(side="right", padx=10)
        
        # Reset Button
        self.reset_btn = ctk.CTkButton(self.top_bar, text="Reset App", width=80, fg_color="#C62828", hover_color="#B71C1C", command=self.reset_app)
        self.reset_btn.pack(side="right", padx=10)

        # Theory Button
        self.theory_btn = ctk.CTkButton(self.top_bar, text="Theory Guide", width=100, command=self.open_theory)
        self.theory_btn.pack(side="right", padx=10)

        # --- Status Bar ---
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.pack(side="bottom", fill="x")
        self.status_label = ctk.CTkLabel(self.status_bar, text="Ready", font=("Roboto", 12))
        self.status_label.pack(side="left", padx=10, pady=2)
        
        self.progress_bar = ctk.CTkProgressBar(self.status_bar, width=200, mode="indeterminate")
        # Hidden by default

        # --- Main Layout (Resizable) ---
        # Using tk.PanedWindow for resizability.
        # FIX: We must wrap ctk widgets in standard tk.Frame when adding to tk.PanedWindow
        # to avoid internal path/geometry manager conflicts.
        self.main_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#2b2b2b", sashwidth=6)
        self.main_paned.pack(fill="both", expand=True)

        # Left Pane: Sidebar (Controls)
        # Wrapper
        self.sidebar_wrapper = tk.Frame(self.main_paned, bg="#2b2b2b")
        self.main_paned.add(self.sidebar_wrapper, stretch="always")
        
        # Actual Content
        self.sidebar = ctk.CTkScrollableFrame(self.sidebar_wrapper, width=400, corner_radius=0)
        self.sidebar.pack(fill="both", expand=True)

        # Right Pane: Visualizations
        # This is a tk widget, so it can be added directly
        self.right_paned = tk.PanedWindow(self.main_paned, orient=tk.VERTICAL, bg="#2b2b2b", sashwidth=6)
        self.main_paned.add(self.right_paned, stretch="always")
        
        # Top Viz Info
        self.viz_top_wrapper = tk.Frame(self.right_paned, bg="#2b2b2b")
        self.right_paned.add(self.viz_top_wrapper, stretch="always", height=400)
        
        self.viz_top_frame = ctk.CTkFrame(self.viz_top_wrapper, corner_radius=0)
        self.viz_top_frame.pack(fill="both", expand=True)
        
        # Bottom Viz Info
        self.viz_bottom_wrapper = tk.Frame(self.right_paned, bg="#2b2b2b")
        self.right_paned.add(self.viz_bottom_wrapper, stretch="always")

        self.viz_bottom_frame = ctk.CTkFrame(self.viz_bottom_wrapper, corner_radius=0)
        self.viz_bottom_frame.pack(fill="both", expand=True)

        # --- Content ---
        self.create_tabs()
        
    def create_tabs(self):
        self.tab_system = ctk.CTkTabview(self.sidebar)
        self.tab_system.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_circuit = self.tab_system.add("Circuit Builder")
        self.tab_finance = self.tab_system.add("Quantum Finance")
        self.tab_challenges = self.tab_system.add("Challenges")
        
        self.setup_circuit_tab()
        self.setup_finance_tab()
        self.setup_challenge_tab()

    def update_status(self, message, is_loading=False):
        """Thread-safe status update"""
        self.status_label.configure(text=message)
        if is_loading:
            self.progress_bar.pack(side="right", padx=10, pady=5)
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
        self.update()

    def toggle_theme(self):
        if self.theme_switch.get() == "Dark":
            ctk.set_appearance_mode("Dark")
            self.main_paned.configure(bg="#2b2b2b")
            self.right_paned.configure(bg="#2b2b2b")
            plt.style.use('dark_background')
        else:
            ctk.set_appearance_mode("Light")
            self.main_paned.configure(bg="#d3d3d3")
            self.right_paned.configure(bg="#d3d3d3")
            plt.style.use('default')
        
        # Re-render plots to match theme if they exist
        # (Simplified: typically you'd trigger a redraw here)

    # ==========================
    # CIRCUIT BUILDER TAB
    # ==========================
    def setup_circuit_tab(self):
        # Init
        init_frame = ctk.CTkFrame(self.tab_circuit)
        init_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(init_frame, text="Qubits:").grid(row=0, column=0, padx=5, pady=5)
        self.qubit_entry = ctk.CTkEntry(init_frame, width=60)
        self.qubit_entry.insert(0, "2")
        self.qubit_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkButton(init_frame, text="Create", width=80, command=self.create_circuit).grid(row=0, column=2, padx=5, pady=5)
        
        # Presets
        ctk.CTkLabel(init_frame, text="Preset:").grid(row=1, column=0, padx=5, pady=5)
        self.algo_combo = ctk.CTkComboBox(init_frame, values=["Bell State", "GHZ State", "Teleportation"], width=120)
        self.algo_combo.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        ctk.CTkButton(init_frame, text="Load", width=80, command=self.load_algorithm).grid(row=1, column=3, padx=5, pady=5)

        # Gates
        self.ops_frame = ctk.CTkFrame(self.tab_circuit)
        self.ops_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(self.ops_frame, text="Gate Operations", font=("Roboto", 14, "bold")).pack(pady=5)
        
        self.gate_var = tk.StringVar(value="H")
        gates = ["H", "X", "Y", "Z", "S", "T", "RX", "RY", "RZ", "CX", "SWAP"]
        
        # Grid layout for gates
        gate_grid = ctk.CTkFrame(self.ops_frame, fg_color="transparent")
        gate_grid.pack()
        for i, gate in enumerate(gates):
            row = 0 if i < 6 else 1
            col = i if i < 6 else i - 6
            ctk.CTkRadioButton(gate_grid, text=gate, variable=self.gate_var, value=gate, command=self.on_gate_select).grid(row=row, column=col, padx=5, pady=5)

        # Params
        param_frame = ctk.CTkFrame(self.ops_frame, fg_color="transparent")
        param_frame.pack(pady=10)
        
        ctk.CTkLabel(param_frame, text="Idx 1:").grid(row=0, column=0)
        self.idx1_entry = ctk.CTkEntry(param_frame, width=50)
        self.idx1_entry.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(param_frame, text="Idx 2:").grid(row=0, column=2)
        self.idx2_entry = ctk.CTkEntry(param_frame, width=50)
        self.idx2_entry.grid(row=0, column=3, padx=5)
        
        ctk.CTkLabel(param_frame, text="Theta:").grid(row=0, column=4)
        self.theta_entry = ctk.CTkEntry(param_frame, width=50)
        self.theta_entry.grid(row=0, column=5, padx=5)
        self.theta_entry.insert(0, "3.14")
        
        ctk.CTkButton(self.ops_frame, text="Add Gate", fg_color="green", command=self.add_gate).pack(pady=10)
        
        # Execution
        exec_frame = ctk.CTkFrame(self.tab_circuit)
        exec_frame.pack(fill="x", pady=20)
        ctk.CTkButton(exec_frame, text="Visualize Circuit", command=self.visualize_circ).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(exec_frame, text="Run Simulation", fg_color="#D32F2F", command=self.start_sim_thread).pack(fill="x", padx=10, pady=5)
        # Educational feature
        ctk.CTkButton(exec_frame, text="View Bloch Spheres (State)", fg_color="#7B1FA2", command=self.start_bloch_thread).pack(fill="x", padx=10, pady=5)
        
        # Add Stepping UI
        self.setup_step_controls(self.tab_circuit)

        self.on_gate_select() # Init state

    def start_bloch_thread(self):
        self.update_status("Calculating Statevector...", is_loading=True)
        thread = threading.Thread(target=self.bloch_task)
        thread.daemon = True
        thread.start()

    def bloch_task(self):
        try:
            sv = self.controller.get_circuit_statevector()
            self.after(0, lambda: self.finish_bloch(sv))
        except Exception as e:
            self.after(0, lambda: self.update_status(f"Bloch Error: {e}"))

    def finish_bloch(self, statevector):
        self.update_status("Statevector Calculated.")
        
        # Plot Bloch
        plt.style.use("default") # Bloch uses white bg usually
        fig = QuantumVisualizer.plot_bloch(statevector)
        
        # We might need to resize it or create a new window if it's too big, 
        # but for now lets try embedding it in the bottom frame (replacing histogram)
        self.embed_figure(fig, self.viz_bottom_frame)


    def on_gate_select(self):
        gate = self.gate_var.get()
        # Logic to enable/disable entries (simulated by changing color or state if supported)
        # ctk entries support state="disabled" or "normal"
        if gate in ["RX", "RY", "RZ"]:
            self.theta_entry.configure(state="normal")
        else:
            self.theta_entry.configure(state="disabled")
            
        if gate in ["CX", "SWAP"]:
            self.idx2_entry.configure(state="normal")
        else:
            self.idx2_entry.configure(state="disabled")

    def create_circuit(self):
        try:
            n = int(self.qubit_entry.get())
            self.controller.create_circuit(n)
            self.update_status(f"Created new circuit with {n} qubits.")
            self.visualize_circ()
        except ValueError:
            self.update_status("Error: Invalid qubit number.")

    def load_algorithm(self):
        algo = self.algo_combo.get()
        if algo == "Bell State": self.controller.create_bell_state()
        elif algo == "GHZ State": self.controller.create_ghz_state()
        elif algo == "Teleportation": self.controller.create_teleportation_circuit()
        self.visualize_circ()
        self.update_status(f"Loaded {algo}.")

    def add_gate(self):
        try:
            gate = self.gate_var.get()
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
            
            self.update_status(f"Added {gate} gate.")
            self.visualize_circ() # Auto-refresh diagram on edit
        except Exception as e:
            self.update_status(f"Error adding gate: {e}")

            self.visualize_circ() # Auto-refresh diagram on edit
        except Exception as e:
            self.update_status(f"Error adding gate: {e}")

    # ==========================
    # STEPPING / DEBUGGING UI
    # ==========================
    def setup_step_controls(self, parent):
        self.step_frame = ctk.CTkFrame(parent)
        self.step_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(self.step_frame, text="Interactive Debugger").pack(pady=5)
        
        controls = ctk.CTkFrame(self.step_frame, fg_color="transparent")
        controls.pack()
        
        self.btn_debug = ctk.CTkButton(controls, text="Start Debug", width=80, command=self.toggle_debug)
        self.btn_debug.grid(row=0, column=0, padx=5)
        
        self.btn_prev = ctk.CTkButton(controls, text="<<", width=40, state="disabled", command=self.on_prev_step)
        self.btn_prev.grid(row=0, column=1, padx=5)
        
        self.step_label = ctk.CTkLabel(controls, text="Step: 0")
        self.step_label.grid(row=0, column=2, padx=5)
        
        self.btn_next = ctk.CTkButton(controls, text=">>", width=40, state="disabled", command=self.on_next_step)
        self.btn_next.grid(row=0, column=3, padx=5)
        
    def toggle_debug(self):
        if not self.controller.current_circuit: return
        
        is_active = not self.controller.step_mode
        self.controller.toggle_step_mode(is_active)
        
        if is_active:
            self.btn_debug.configure(text="Stop", fg_color="red")
            self.btn_prev.configure(state="normal")
            self.btn_next.configure(state="normal")
        else:
            self.btn_debug.configure(text="Start Debug", fg_color=["#3B8ED0", "#1F6AA5"])
            self.btn_prev.configure(state="disabled")
            self.btn_next.configure(state="disabled")
            
        self.refresh_step_view()
        
    def on_next_step(self):
        self.controller.step_forward()
        self.refresh_step_view()
        
    def on_prev_step(self):
        self.controller.step_backward()
        self.refresh_step_view()
        
    def refresh_step_view(self):
        self.step_label.configure(text=f"Step: {self.controller.current_step}")
        self.visualize_circ()
        # Also auto-update Bloch if we are in debug mode? Yes, that's the point.
        if self.controller.step_mode:
            self.start_bloch_thread()

    # ==========================
    # FINANCE TAB
    # ==========================
    def setup_finance_tab(self):
        # Stock Input
        input_frame = ctk.CTkFrame(self.tab_finance)
        input_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(input_frame, text="Stock Symbol:").grid(row=0, column=0, padx=5)
        self.stock_combo = ctk.CTkComboBox(input_frame, values=self.finance_controller.get_available_stocks())
        self.stock_combo.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(input_frame, text="Days:").grid(row=0, column=2, padx=5)
        self.days_entry = ctk.CTkEntry(input_frame, width=50)
        self.days_entry.insert(0, "10")
        self.days_entry.grid(row=0, column=3, padx=5)
        
        ctk.CTkButton(input_frame, text="Load Data", command=self.start_load_stock_thread).grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        # Encoding
        enc_frame = ctk.CTkFrame(self.tab_finance)
        enc_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(enc_frame, text="Encoding Strategy").pack()
        
        self.enc_var = tk.StringVar(value="angle")
        ctk.CTkRadioButton(enc_frame, text="Angle Encoding", variable=self.enc_var, value="angle").pack(pady=2)
        ctk.CTkRadioButton(enc_frame, text="Correlated (CX)", variable=self.enc_var, value="correlated").pack(pady=2)
        
        ctk.CTkButton(enc_frame, text="Generate Circuit", command=self.generate_finance_circuit).pack(pady=10, fill="x")

    # ==========================
    # WORKER THREADS
    # ==========================
    def start_sim_thread(self):
        self.update_status("Running Simulation...", is_loading=True)
        thread = threading.Thread(target=self.run_simulation_task)
        thread.daemon = True
        thread.start()

    def run_simulation_task(self):
        try:
            self.controller.current_circuit.measure_all()
            counts, _ = self.controller.run_simulation()
            
            # Post back to UI thread
            self.after(0, lambda: self.finish_simulation(counts))
        except Exception as e:
            self.after(0, lambda: self.update_status(f"Sim Error: {e}"))

    def finish_simulation(self, counts):
        self.update_status("Simulation Complete.")
        
        # Plot Histogram
        plt.style.use("dark_background" if self.theme_switch.get() == "Dark" else "default")
        fig = QuantumVisualizer.plot_results(counts)
        self.embed_figure(fig, self.viz_bottom_frame)

    def start_load_stock_thread(self):
        self.update_status("Fetching Stock Data...", is_loading=True)
        thread = threading.Thread(target=self.load_stock_task)
        thread.daemon = True
        thread.start()
        
    def load_stock_task(self):
        try:
            symbol = self.stock_combo.get()
            days = int(self.days_entry.get())
            data = self.finance_controller.load_stock_data(symbol, days)
            self.after(0, lambda: self.finish_stock_load(data))
        except Exception as e:
            self.after(0, lambda: self.update_status(f"Data Error: {e}"))

    def finish_stock_load(self, data):
        self.update_status(f"Loaded {len(data.prices)} days for {data.symbol}")
        
        # Plot
        plt.style.use("dark_background" if self.theme_switch.get() == "Dark" else "default")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(data.dates, data.prices, marker='o', color="#4FC3F7") # Light blue
        ax.set_title(f"{data.symbol} Stock Price")
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        
        self.embed_figure(fig, self.viz_top_frame)

    def generate_finance_circuit(self):
        if self.finance_controller.current_stock_data is None:
            self.update_status("Load stock data first!")
            return

        encoding = self.enc_var.get()
        if encoding == "angle":
            self.controller.current_circuit = self.finance_controller.create_angle_encoded_circuit()
        else:
            self.controller.current_circuit = self.finance_controller.create_correlated_circuit()
            
        self.visualize_circ()
        self.update_status(f"Generated {encoding} circuit.")

        self.visualize_circ()
        self.update_status(f"Generated {encoding} circuit.")

    # ==========================
    # CHALLENGE TAB
    # ==========================
    def setup_challenge_tab(self):
        # 1. Challenge Selector
        sel_frame = ctk.CTkFrame(self.tab_challenges)
        sel_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(sel_frame, text="Select Challenge:").pack(pady=5)
        self.challenge_combo = ctk.CTkComboBox(sel_frame, values=self.challenge_manager.get_challenges(), width=250, command=self.on_challenge_select)
        self.challenge_combo.pack(pady=5)
        
        # 2. Description
        self.desc_frame = ctk.CTkFrame(self.tab_challenges)
        self.desc_frame.pack(fill="both", expand=True, pady=10)
        
        self.desc_label = ctk.CTkLabel(self.desc_frame, text="Select a challenge to begin...", wraplength=350, justify="left")
        self.desc_label.pack(padx=10, pady=10)
        
        # 3. Actions
        act_frame = ctk.CTkFrame(self.tab_challenges)
        act_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(act_frame, text="Load Challenge", command=self.load_challenge).pack(pady=5, fill="x")
        ctk.CTkButton(act_frame, text="Verify Solution", fg_color="green", command=self.check_challenge_solution).pack(pady=5, fill="x")

    def on_challenge_select(self, choice):
        # Just update desc
        # choice format "key: name"
        pass 

    def load_challenge(self):
        choice = self.challenge_combo.get()
        challenge = self.challenge_manager.set_challenge(choice)
        
        if challenge:
            self.desc_label.configure(text=f"GOAL: {challenge['description']}\n\nTarget Details:\nQubits: {challenge['qubits']}")
            
            # Reset circuit to match challenge requirements
            self.controller.create_circuit(challenge["qubits"])
            self.update_status(f"Started Challenge: {challenge['name']}")
            self.visualize_circ()
            
            # Switch to circuit tab to let them work
            self.tab_system.set("Circuit Builder")
        
    def check_challenge_solution(self):
        if not self.controller.current_circuit:
            self.update_status("No circuit to check.")
            return

        success, msg = self.challenge_manager.check_solution(self.controller.current_circuit)
        
        if success:
            messagebox.showinfo("Challenge Success!", f"Congratulations!\n\n{msg}")
            self.update_status("Challenge Complete!")
        else:
            messagebox.showerror("Try Again", f"{msg}")
            self.update_status("Verification Failed.")
    def reset_app(self):
        # 1. Reset Circuit Tab
        self.controller.create_circuit(2) # Default 2 qubits
        self.qubit_entry.delete(0, tk.END)
        self.qubit_entry.insert(0, "2")
        self.idx1_entry.delete(0, tk.END)
        self.idx2_entry.delete(0, tk.END)
        self.theta_entry.delete(0, tk.END)
        self.theta_entry.insert(0, "3.14")
        self.algo_combo.set("")
        
        # 2. Reset Finance Tab
        self.finance_controller.current_stock_data = None
        self.stock_combo.set(self.finance_controller.get_available_stocks()[0])
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, "10")
        
        # 3. Clear Visuals
        self.clear_visuals()
        
        self.update_status("Application Reset.")

    def clear_visuals(self):
        # Clear specific frames
        for widget in self.viz_top_frame.winfo_children(): widget.destroy()
        for widget in self.viz_bottom_frame.winfo_children(): widget.destroy()

    # ==========================
    # VISUALIZATION HELPERS
    # ==========================
    def visualize_circ(self):
        # Use pure translation for visualization (no simulation required)
        # This prevents "No counts" errors when constructing circuits without measurements
        
        # FIX: Use get_active_circuit() to support Stepping Mode
        circuit_to_show = self.controller.get_active_circuit()
        if not circuit_to_show: return

        q_circ = QiskitEngine.translate_to_qiskit(circuit_to_show)
        
        # Plot
        plt.style.use("default") 
        fig = QuantumVisualizer.show_circuit_diagram(q_circ)
        self.embed_figure(fig, self.viz_top_frame)

    def embed_figure(self, fig, parent_frame):
        # Clear old
        for widget in parent_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        
        # Add Cursor Interactivity
        cursor = mplcursors.cursor(fig.get_axes()[0], hover=True)
        
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def open_theory(self):
        """Open the THEORY.md file in the default browser/viewer"""
        try:
            # Assume we are in root (main.py execution)
            path = os.path.abspath("THEORY.md")
            if not os.path.exists(path):
                # Fallback: maybe we are running from inside module
                path = os.path.abspath("../../THEORY.md")
            
            webbrowser.open(path)
            self.update_status("Opened Theory Guide.")
        except Exception as e:
            self.update_status(f"Error opening help: {e}")

def launch_gui():
    app = QuantumGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()
