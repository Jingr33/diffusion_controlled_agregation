import config
import numpy as np
import math
import random

class LayoutGenerator ():
    def __init__(self, layout : str, atoms_num : int):
        self.atoms_num = atoms_num      
        if (layout == config.layout_choices[0]):
            self.start_postions = self._gen_cube_layout()
        elif (layout == config.layout_choices[1]):
            self.start_postions = self._gen_sphere_layout()
        elif (layout == config.layout_choices[2]):
            self.start_postions = self._gen_random_layout()
        
    def _gen_cube_layout(self) -> list:
        coord_list = [None] * self.atoms_num
        half_edge = np.pow(self.atoms_num, 0.56)
        for i in range(self.atoms_num):
            rnd_coord = random.randint(0, 2)
            rnd_side = random.choice([-1, 1])
            position = np.array([0.0, 0.0, 0.0])
            position[rnd_coord] = half_edge * rnd_side
            for j in range(len(position)):
                if (position[j] != 0): continue
                position[j] = random.uniform(-half_edge, half_edge)
            coord_list[i] = position
        return coord_list

    def _gen_sphere_layout(self) -> list:
        coord_list = [None] * self.atoms_num
        r = np.pow(self.atoms_num, 0.5) * 2
        for i in range(self.atoms_num):
            phi = random.uniform(0, np.pi)
            theta = random.uniform(0, 2*np.pi)
            x = r * np.cos(phi) * np.sin(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(theta)
            coord_list[i] = np.array([x, y, z])
        return coord_list

    def _gen_random_layout(self) -> list:
        max_radius = math.ceil(math.pow(self.atoms_num, 0.5))
        coord_list = [None] * self.atoms_num
        for i in range(self.atoms_num):
            x = random.randint(-max_radius, max_radius + 1)
            y = random.randint(-max_radius, max_radius + 1)
            z = random.randint(-max_radius, max_radius + 1)
            coord_list[i] = np.array([x, y, z])
        return coord_list
    
    def get_start_pos (self) -> list:
        return self.start_postions
