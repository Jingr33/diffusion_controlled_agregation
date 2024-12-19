from vispy import scene
from vispy.visuals.transforms import STTransform

from Calculation import Calculation
from config import *


class Atom ():
    def __init__(self, type : str, position : tuple):
        self.type = type
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.z_pos = position[2]
        self.color = self._set_fg_color()

    def _set_fg_color (self):
        if (self.type == "ion"):
            return ion_color
        return electrode_color
        
    def display(self, view) -> None:
        self.sphere = scene.visuals.Sphere(radius=1, method='ico', parent=view.scene, color = self.color, edge_color = atom_edge_color, subdivisions=2)
        self.translate()

    def update(self, view) -> None:
        self.x_pos, self.y_pos, self.z_pos = Calculation.update_postion((self.x_pos, self.y_pos, self.z_pos))
        self.translate()

    def translate (self) -> None:
        self.sphere.transform = STTransform(translate=[self.x_pos, self.y_pos, self.z_pos])
