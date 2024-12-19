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
        pass

    def _gen_sphere_layout(self) -> list:
        pass

    def _gen_random_layout(self) -> list:
        max_radius = math.ceil(math.pow(self.atoms_num, 0.8))
        coord_list = [None] * self.atoms_num
        for i in range(self.atoms_num):
            y_coord = random.randint(-max_radius, max_radius + 1)
            z_coord = random.randint(-max_radius, max_radius + 1)
            x_coord = random.randint(-max_radius, max_radius + 1)
            coord_list[i] = (x_coord, y_coord, z_coord)
        return coord_list
    
    def get_start_pos (self) -> list:
        return self.start_postions
