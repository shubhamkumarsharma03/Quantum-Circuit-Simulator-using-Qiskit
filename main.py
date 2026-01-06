import sys
import argparse
from quantum_simulator.presentation.cli import main_menu
from quantum_simulator.presentation.gui import launch_gui

def main():
    parser = argparse.ArgumentParser(description="Industry-Grade Quantum Circuit Simulator")
    parser.add_argument("--gui", action="store_true", help="Launch the Graphical User Interface")
    args = parser.parse_args()

    if args.gui:
        launch_gui()
    else:
        main_menu()

if __name__ == "__main__":
    main()
