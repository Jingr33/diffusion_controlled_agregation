from vispy import scene
from vispy.visuals.transforms import STTransform
from vispy.app import Timer
import imageio
from icecream import ic
import threading

from Layout_generator import LayoutGenerator
from Calculation import Calculation
from Atom import Atom
import config

class Simulation ():
    def __init__(self, layout : str, atoms_num : int, save : bool):
        self.layout = layout
        self.save = save
        self.atoms_num = atoms_num
        self.freeze_atoms = []
        self.moving_atoms = []
        self.atoms = []
        self._generate_ion_layout()
        self.electrode = self._generate_elecrode()
        self._calculate_simulation()
        self._init_scene()
        self._display_sim_state("start", self.vb1)
        self._display_sim_state("finish", self.vb2)


        # self.electrode.display(self.view)
        # self.timer = Timer(interval = config.time_step, connect = self._update, start = True)
        # self.timer.start()

    def _init_scene(self) -> None:
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                           size=(1200, 750), show=True, fullscreen=True)
        # self.view = self.canvas.central_widget.add_view()
        self.vb1 = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
        self.vb2 = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
        # grid
        grid = self.canvas.central_widget.add_grid()
        grid.padding = 10
        grid.add_widget(self.vb1, 0, 0)
        grid.add_widget(self.vb2, 0, 1)
        # camera
        # self.view.camera = 'arcball'
        # self.view.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])
        self.vb1.camera = 'arcball'
        self.vb1.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])
        self.vb2.camera = 'arcball'
        self.vb2.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])

    def _display_sim_state (self, time : str, viewbox) -> None:
        self.atoms = self.freeze_atoms + self.moving_atoms
        for atom in self.atoms:
            atom.display(viewbox, time)        

    def _generate_ion_layout (self):
        layout_gen = LayoutGenerator(self.layout, self.atoms_num)
        coords = layout_gen.get_start_pos()
        for i in range(self.atoms_num):
            atom = Atom("ion", coords[i])
            self.moving_atoms.append(atom)

    def _generate_elecrode(self):
        electrode = Atom("electrode", (0, 0, 0))
        self.freeze_atoms.append(electrode)
        return electrode
    

    # def _update(self, event) -> None:
    #     for atom in self.moving_atoms:
    #         atom.update(self.view)

    def _calculate_simulation (self):
        calc = Calculation(self)
        calc.calculate()
        # calc_thread = threading.Thread(target=calc.calculate)
        # calc_thread.start()

    def run(self) -> None:
        self.canvas.app.run()
