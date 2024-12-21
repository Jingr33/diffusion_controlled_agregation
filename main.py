import argparse
from simulation import Simulation
from chart_creator import ChartCreator
from config import *

def main():
    parser = argparse.ArgumentParser(description = "Difuzně řízená agregace")
    parser.add_argument("--layout", type=str, choices = layout_choices, default = layout_default, help = "Typ počátečního rozdělení molekul")
    parser.add_argument("--atoms", nargs='+', type=int, default = atoms_default, help = "Počet atomů v simulaci")
    parser.add_argument("--visualize", type=bool, default=False, help = "Zobrazí vizualizaci počátečního a koncového stavu")
    parser.add_argument("--plot", type=bool, default=True, help = "Zobrazí graf počet atomů vs. gyrační poloměr")
    parser.add_argument("--simulation", type=bool, default = True, help = "Spustí simulaci")

    args = parser.parse_args()
    _start_sim(args.layout, args.atoms, args.visualize, args.simulation)
    _plot_chart(args.plot)

def _start_sim (layout : str, atom_numbers : list, visualize : bool, simulation : bool) -> None:
    if (not simulation): return
    for atom_number in atom_numbers:
        sim = Simulation(layout, atom_number, visualize)
        if (visualize):
            sim.run()

def _plot_chart (plot_bool) -> None:
    if (plot_bool):
        ChartCreator()


if __name__ == '__main__':
    main()