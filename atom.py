from vispy import scene
from vispy.visuals.transforms import STTransform
from vispy.visuals.transforms import MatrixTransform
from vispy.geometry import create_cylinder  

from calculation import Calculation
import config
import numpy as np


class Atom ():
    def __init__(self, type : str, position : np.array):
        self.type = type
        self.position = position
        self.generation = 0 if self.type == "electrode" else -1
        self.orig_generation = self.generation
        self.positions_list = [self.position]
        self.electrode_dist = Calculation.vec_magnitude(Calculation.opposite_direction(self.position))
        self.parent_electrode = None
            
    def display(self, view, sim_time : str) -> None:
        generation = self.generation if sim_time != "start" else self.orig_generation
        position = self.positions_list[0] if sim_time == "start" else self.positions_list[-1]
        self.color = self._set_fg_color(generation)
        self.sphere = scene.visuals.Sphere(radius=config.atom_radius, method='ico', parent=view.scene, color = self.color, edge_color = config.atom_edge_color)
        self._translate_sphere(position)

    def _set_fg_color (self, generation : int):
        if (generation == -1):
            return config.atom_color[-1]
        return config.atom_color[generation % 10]

    def update_position(self, new_position : np.array) -> None:
        self.position = new_position
        self.positions_list.append(new_position)

    def _translate_sphere (self, pos : np.array) -> None:
        self.sphere.transform = STTransform(translate=[pos[0], pos[1], pos[2]])

    def _translate_line(self, self_position : np.array) -> None:
        center = self.parent_electrode.position - self_position
        pos = self_position + center
        self.line.transform = STTransform(translate=[pos[0], pos[1], pos[2]])

    def transform_to_electrode (self, nearest_electrode) -> None:
        self.type = "electrode"
        self.parent_electrode = nearest_electrode
        self.generation = self.parent_electrode.generation + 1
        new_pos = Calculation.final_pos_optimalization(self)
        self.update_position(new_pos)
