import matplotlib.pyplot as plt
import numpy as np


class ChartCreator ():
    """
    Create chart in the end of app run.

    Chart content:
        log N (number of particled in simulation) vs. log Rg (gyration radius)
        fractal dimension of dendrimers created from some layout
    """

    def __init__(self):
        """
        Initialize chart creator.
        """
        self.atoms_numbers = []
        self.gyrations = []
        self._load_data()
        self._calc_data()
        self._plot()

    def _load_data (self) -> None:
        """
        Load data from a database.
        """
        lines = []
        with open ("database_cube.txt", "r+") as f:
            lines = f.readlines()
        for line in lines:
            data = line.split(" ")
            self.gyrations.append(float(data[0]))
            self.atoms_numbers.append(int(data[1]))

    def _calc_data (self) -> None:
        """
        Prepares data for the chart and calculates  fractal dimension fo the dendrimers.
        """
        self.log_N = np.log10(self.atoms_numbers)
        self.log_Rg = np.log10(self.gyrations)
        coeffs = np.polyfit(self.log_Rg, self.log_N, 1)
        self.p = np.poly1d(coeffs)
        self.fractal_dimension = np.round(coeffs[0], 4)

    def _plot(self) -> None:
        """
        Plot data.
        """
        plt.scatter(self.log_Rg, self.log_N, color="#3288bd")
        plt.plot(self.log_Rg, self.p(self.log_Rg), linestyle="dotted")
        plt.title(f"Závislost logaritmu počtu atomů na logaritmu gyračního poloměru\nFraktální dimenze Df = {self.fractal_dimension}")
        plt.xlabel("log Rg")
        plt.ylabel("log N")
        plt.show()
