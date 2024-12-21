import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class ChartCreator ():
    def __init__(self):
        self.atoms_numbers = []
        self.gyrations = []
        self._load_data()
        self._plot()

    def _load_data (self) -> None:
        lines = []
        with open ("database.txt", "r+") as f:
            lines = f.readlines()
        for line in lines:
            data = line.split(" ")
            self.gyrations.append(float(data[0]))
            self.atoms_numbers.append(int(data[1]))

    def _plot(self) -> None:
        self.log_atom_nums = [np.log10(num) for num in self.atoms_numbers]
        self.log_gyrations = [np.log10(gyr) for gyr in self.gyrations]
        plt.scatter(self.log_gyrations, self.log_atom_nums, color="blue")
        plt.title("Závislost logaritmu počtu atomů na logaritmu gyračního poloměru")
        plt.xlabel("log Rg")
        plt.ylabel("log N")
        plt.show()
