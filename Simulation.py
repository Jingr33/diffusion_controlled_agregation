from vispy import scene
from vispy.visuals.transforms import STTransform
import imageio
import numpy as np
from icecream import ic

from layout_generator import LayoutGenerator
from calculation import Calculation
from atom import Atom

class Simulation ():
    def __init__(self, layout : str, atoms_num : int, save : bool):
        self.layout = layout
        self.save = save
        self.atoms_num = atoms_num
        self.ions = []
        self.electrodes = []
        self.atoms = []
        self._generate_ion_layout()
        self.electrode = self._generate_elecrode()
        self._calculate_simulation()
        self._init_scene()
        self._display_sim_state("start", self.vb1)
        self._display_sim_state("finish", self.vb2)

    def _init_scene(self) -> None:
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
        self.atoms = self.ions + self.electrodes
        for atom in self.atoms:
            atom.display(viewbox, sim_time)        

    def _generate_ion_layout (self):
        layout_gen = LayoutGenerator(self.layout, self.atoms_num)
        coords = layout_gen.get_start_pos()
        for i in range(self.atoms_num):
            atom = Atom("ion", coords[i])
            self.ions.append(atom)

    def _generate_elecrode(self):
        electrode = Atom("electrode", np.array([0, 0, 0]))
        electrode.parent_electrode = electrode
        self.ions.append(electrode)
        return electrode
    
    def _calculate_simulation (self):
        calc = Calculation(self)
        calc.calculate_sim()

    def run(self) -> None:
        self.canvas.app.run()
