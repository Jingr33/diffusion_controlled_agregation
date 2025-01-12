"""
App for simulation of diffusion controlled agregation. It simulates the creation of a dendrimer during electrolysis.
"""


import argparse # zpracování argumetů z konzole
from Simulation import Simulation
from chart_creator import ChartCreator
from config import *

def main():
    parser = argparse.ArgumentParser(description = "Difuzně řízená agregace")
    parser.add_argument("--layout", type=str, choices = layout_choices, default = layout_default, help = "Typ počátečního rozdělení molekul")
    parser.add_argument("--atoms", nargs='+', type=int, default = atoms_default, help = "Počet atomů v simulaci")
    parser.add_argument("--visualize", action="store_true", help = "Zobrazí vizualizaci počátečního a koncového stavu")
    parser.add_argument("--plot", action="store_true", help = "Zobrazí graf počet atomů vs. gyrační poloměr")
    parser.add_argument("--sim", action="store_true", help = "Spustí simulaci")

    args = parser.parse_args()
    _start_sim(args.layout, args.atoms, args.visualize, args.sim)
    _plot_chart(args.plot)

def _start_sim (layout : str, atom_numbers : list, visualize : bool, simulation : bool) -> None:
    """
    Start simulation and visualization

    Performs the entire simulation, followed by visualization and calculation of gyraion radius of the system.

    Args:
        layout (str): Start positions of the ions (cube, sphere or random layout)
        atom_numbers (int): number of ions in the simulation
        visualize (bool): if the visualization of start and finished state is enabled
        simulation (bool): if the simulation process is enabled
    """
    if not simulation: return
    for atom_number in atom_numbers:
        sim = Simulation(layout, atom_number, visualize)
        if (visualize):
            sim.run()

def _plot_chart (plot : bool) -> None:
    """
    Plot chart.

    Plots a dependency graph of log N (particles number) on log Rg (gyration radius) after the simulation is terminated.

    Args:
        plot (bool): Plot of chart is enabled.
    """
    if (plot):
        ChartCreator()


if __name__ == '__main__':
    main()