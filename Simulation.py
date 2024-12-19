from vispy import scene
from vispy.visuals.transforms import STTransform
from vispy.app import Timer
import imageio
from icecream import ic

from Layout_generator import LayoutGenerator
from Atom import Atom
import config

class Simulation ():
    def __init__(self, layout : str, atoms_num : int, save : bool):
        self.layout = layout
        self.save = save
        self.atoms_num = atoms_num
        self._init_scene()
        self.electrode = self._generate_elecrode()
        self.electrode.display(self.view)
        self.moving_atoms = []
        self.freeze_atoms = [self.electrode]
        self._generate_layout()
        self.timer = Timer(interval = config.time_step, connect = self._update, start = True)
        self.timer.start()

    def _init_scene(self) -> None:
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                           size=(800, 600), show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'arcball'
        self.view.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])

    def _generate_layout (self):
        layout_gen = LayoutGenerator(self.layout, self.atoms_num)
        coords = layout_gen.get_start_pos()
        for i in range(self.atoms_num):
            atom = Atom("ion", coords[i])
            self.moving_atoms.append(atom)
            atom.display(self.view)
        pass

    def _generate_elecrode(self):
        return Atom("electrode", (0, 0, 0))

    def _update(self, event) -> None:
        for atom in self.moving_atoms:
            atom.update(self.view)

    def run(self) -> None:
        self.canvas.app.run()
