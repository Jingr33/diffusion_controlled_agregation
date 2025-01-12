from vispy import scene
import numpy as np

from layout_generator import LayoutGenerator
from calculation import Calculation
from atom import Atom


class Simulation ():
    """
    Class for managing simulation of the creation of the dendrimer and visualization of the process.

    Attributtes:
        layout (str): Starting layout of the free ions in the space
        atoms_num (int): number of atoms in sim
        ions (list): list of all ions in sim
        electrodes (list): list of all electrodes in sim
        _radius_of_gyration (float): gyration radius of the created dendrimer
        canvas (scene): canvas of the visualization
        vb1: viewbox 1
        vb2: viewbox 2
    """
    def __init__(self, layout : str, atoms_num : int, visualize : bool) -> None:
        """
        Initialize Simulation

        Args:
            layout (str): Starting layout of the simulation
            atoms_num (int): number of atoms in the simulation
            viualize (bool): if the visualization is enabled
        """
        self.layout = layout
        self.atoms_num = atoms_num
        self.ions = []
        self.electrodes = []
        self.atoms = []
        self._generate_ion_layout()
        self.electrode = self._generate_elecrode()
        self._calculate_simulation()
        if (visualize): self._visualize()
        self._radius_of_gyration = self._calc_gyration()
        self._gyration_to_db()

    def _visualize(self) -> None:
        """
        Visualize start and end point of the simulation at the end of the process (if it is enabled).
        """
        self._init_scene()
        self._display_sim_state("start", self.vb1)
        self._display_sim_state("finish", self.vb2)

    def _init_scene(self) -> None:
        """
        Initialize scene (canvas and viewboxes) for visualization of simulation.
        """
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                           size=(1200, 750), show=True, fullscreen=True)
        self.vb1 = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
        self.vb2 = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
        # grid
        grid = self.canvas.central_widget.add_grid()
        grid.padding = 10
        grid.add_widget(self.vb1, 0, 0)
        grid.add_widget(self.vb2, 0, 1)
        # camera
        self.vb1.camera = 'arcball'
        self.vb1.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])
        self.vb2.camera = 'arcball'
        self.vb2.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])

    def _display_sim_state (self, sim_time : str, viewbox) -> None:
        """
        Dispaly elected state of the simulation in the viewbox

        Args:
            sim_time (str): time state of the simulation
            viewbox: viewbox of the scene
        """
        self.atoms = self.ions + self.electrodes
        for atom in self.atoms:
            atom.display(viewbox, sim_time)        

    def _generate_ion_layout (self) -> None:
        """
        Generate initial layout of atoms in the space (through layout generator).
        """
        layout_gen = LayoutGenerator(self.layout, self.atoms_num)
        coords = layout_gen.get_start_pos()
        for i in range(self.atoms_num):
            atom = Atom("ion", coords[i])
            self.ions.append(atom)

    def _generate_elecrode(self) -> Atom:
        """
        Create first electrode in the before start of the simulation.

        Returns:
            Atom: electrode in the (0, 0, 0) postion
        """
        electrode = Atom("electrode", np.array([0, 0, 0]))
        electrode.parent_electrode = electrode
        self.ions.append(electrode)
        return electrode
    
    def _calculate_simulation (self) -> None:
        """
        Calculate simulation (through a Calculation class).
        """
        calc = Calculation(self)
        calc.calculate_sim()

    def run(self) -> None:
        """
        Start visualization of simulation.
        """
        self.canvas.app.run()

    def _calc_gyration (self) -> float:
        """
        Calculates radius of gyration of the molecule.

        Returns:
            float: radius of the gyration
        """
        atoms = self.electrodes + self.ions
        com = self._center_of_mass(atoms)
        r_pow2_sum = 0
        for atom in atoms:
            r_atom = np.linalg.norm(atom.position - com)
            r_pow2_sum += np.pow(r_atom, 2)
        return np.sqrt(r_pow2_sum / self.atoms_num)

    def _center_of_mass (self, atoms : list) -> np.array:
        """
        Calculates a center of mass of the molecule.

        Args:
            atoms (list): list of all atoms in simulation

        Returns:
            np.array: a center of mass position
        """
        pos_sum = np.array([0, 0, 0])
        for atom in atoms:
            pos_sum = pos_sum + atom.position
        return np.array(pos_sum / self.atoms_num)

    def _gyration_to_db (self) -> None:
        """
        Save N and Rg to a database.
        """
        with open ("database.txt", "a+") as f:
            line = f"{self._radius_of_gyration} {self.atoms_num}\n"
            f.write(line)