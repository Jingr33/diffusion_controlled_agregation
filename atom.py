from vispy import scene # visualization of simulations
from vispy.visuals.transforms import STTransform
from typing import Any

from calculation import Calculation
import config
import numpy as np


class Atom ():
    """
    Representation of one atom (particle) in simulation.

    Attributes:
        type (str): electrode or ion
        position (np.array): 3D position of the atom in a space
        generation (int): generation of particle in dendrimer
        positions_list (list): list of all positions during simulation
        electrode_dist (float): distance to nearest electrode postion
        parent_electrode (Atom): Ion -> None, Electrode -> neighboring electrode with lower genreation
    """
    def __init__(self, type : str, position : np.array) -> None:
        """
        Initialize an atom.

        Args:
            type (str): electrode or ion
            position (np.array): 3D position of the atom in a space
        """
        self.type = type
        self.position = position
        self.generation = 0 if self.type == "electrode" else -1
        self.orig_generation = self.generation
        self.positions_list = [self.position]
        self.electrode_dist = Calculation.vec_magnitude(Calculation.opposite_direction(self.position))
        self.parent_electrode = None
            
    def display(self, view, sim_time : str) -> None:
        """
        Display the atom in visualization as a sphere.

        Args:
            view (vispy.scene.visuals): view window of the simulation
            sim_time (str): 'start' or 'finish' (start or end state of the simulation)
        """
        generation = self.generation if sim_time != "start" else self.orig_generation
        position = self.positions_list[0] if sim_time == "start" else self.positions_list[-1]
        self.color = self._set_fg_color(generation)
        self.sphere = scene.visuals.Sphere(radius=config.atom_radius, method='ico', parent=view.scene, color = self.color, edge_color = config.atom_edge_color)
        self._translate_sphere(position)

    def _set_fg_color (self, generation : int) -> Any:
        """
        Set a color of the atom depending on its generation in dendrimer.

        Args:
            generation (int): generation of the particle (if -1, it is a free ion)
        
        Return:
            Any: Color of the atom in format from config file (BGR, HEX, ...)
        """
        if (generation == -1):
            return config.atom_color[-1]
        return config.atom_color[generation % 10]

    def update_position(self, new_position : np.array) -> None:
        """
        Method for updating an atom position.

        Args:
            new_positon (np.array): new 3D position of the atom.
        """
        self.position = new_position
        self.positions_list.append(new_position)

    def _translate_sphere (self, pos : np.array) -> None:
        """
        Set or shift the atom in the entered positon in the space.

        Args:
            pos (np.array): 3D position of the atom in the space.
        """
        self.sphere.transform = STTransform(translate=[pos[0], pos[1], pos[2]])

    def transform_to_electrode (self, nearest_electrode) -> None:
        """
        Transform an ion to a eletrode when bound the dendrimer structure.

        Args:
            nearest_electrode (Atom): nearest (connected) electrode to this atom.
        """
        self.type = "electrode"
        self.parent_electrode = nearest_electrode
        self.generation = self.parent_electrode.generation + 1
        new_pos = Calculation.final_pos_optimalization(self)
        self.update_position(new_pos)
