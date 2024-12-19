import argparse

from simulation import Simulation
from config import *

def main():
    parser = argparse.ArgumentParser(description = "Difuzně řízená agregace")
    parser.add_argument("--layout", type=str, choices = layout_choices, default = layout_default, help = "Typ počátečního rozdělení molekul")
    parser.add_argument("--atoms", type=int, default = atoms_default, help = "Počet atomů v simulaci")
    parser.add_argument("--save", type=bool, choices=[True, False], default = False, help = "Uložení průběhu simulace (gif)")
    args = parser.parse_args()

    sim = Simulation(args.layout, args.atoms, args.save)
    sim.run()

if __name__ == '__main__':
    main()