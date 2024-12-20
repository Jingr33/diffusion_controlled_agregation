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
        self.orig_type = type
        self.position = position
        self.positions_list = [self.position]
        self.electrode_dist = Calculation.vec_magnitude(Calculation.opposite_direction(self.position))
        self.parent_electrode = None
            
    def display(self, view, sim_time : str) -> None:
        type = self.type if sim_time != "start" else self.orig_type
        position = self.positions_list[0] if sim_time == "start" else self.positions_list[-1]
        atom_radius = config.atom_radius if sim_time == "start" else config.atom_radius/2
        self.color = self._set_fg_color(type)
        if (type == "electrode"):
            self._display_electrode(view, position, atom_radius)
        else:
            self._display_ion(view, position, atom_radius)


    def _display_ion (self, view, position, atom_radius) -> None:
        self.sphere = scene.visuals.Sphere(radius=atom_radius, method='ico', parent=view.scene, color = self.color, edge_color = config.atom_edge_color)
        self._translate_sphere(position)

    def _display_electrode (self, view, position, atom_radius) -> None:
        self.sphere = scene.visuals.Sphere(radius=atom_radius, method='ico', parent=view.scene, color = self.color, edge_color = config.atom_edge_color)
        self._translate_sphere(position)

        direction = np.array(self.parent_electrode.position - self.position)
        length = np.linalg.norm(direction)
        direction = direction / length
        mesh_data = create_cylinder(radius=0.2, length=length, rows=10, cols=20)
        cylinder = scene.visuals.Mesh(meshdata=mesh_data, color=self.color, parent=view)
        transform = MatrixTransform()
        transform.translate(self.position)
        # self.line = scene.visuals.Line(pos=points, color=self.color, width=2, parent=view)        
        # self.cylinder = scene.visuals.Cylinder(radius=0.2, length=length, parent=view,
        #                               direction=direction, color=self.color, method='smooth')
        # transform = MatrixTransform()
        # transform.translate(self.position)
        # transform.rotate(np.degrees(np.arccos(direction[2])), [-direction[1], direction[0], 0])
        # self.cylinder.transform = transform
        # self._translate_line(position)

    def _set_fg_color (self, type):
        if (type == "ion"):
            return config.ion_color
        return config.electrode_color

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
