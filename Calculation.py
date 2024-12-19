import random
import config
import numpy as np


class Calculation ():
    def __init__(self, master):
        self.moving_atoms = master.moving_atoms
        self.freeze_atoms = master.freeze_atoms

    def calculate (self):
        count = 0
        while len(self.moving_atoms) != 0 and count < 300:
            for atom in self.moving_atoms:
                shift_vec = self.gen_biased_vector(atom)
                atom.update_position(atom.position + shift_vec)
            print(len(self.freeze_atoms))
            count += 1
            
    def _check_freeze (self, atom) -> None:
        if (atom.freeze_distance > 1):
            atom.reduce_freeze_dist()
            return

        atom.freeze_distance = self._find_shortest_freeze_dist(atom)
        if (atom.freeze_distance <= 1):
            self.freeze_atoms.append(atom)
            self.moving_atoms.remove(atom)

    def _find_shortest_freeze_dist(self, atom) -> float:
        shortest_dist = 1000
        for freeze_atom in self.freeze_atoms:
            actual_distance = np.linalg.norm(atom.position - freeze_atom.position)
            if (actual_distance < shortest_dist):
                shortest_dist = actual_distance
        return shortest_dist

    def gen_biased_vector (self, atom) -> tuple:
        probability = config.direc_prob
        pref_direc = Calculation.opposite_direction(atom.position)
        pref_direc = pref_direc / np.linalg.norm(pref_direc)
        rand_direc = np.random.normal(3)
        rand_direc = rand_direc / np.linalg.norm(rand_direc)
        biased_vec = (1 - probability) * rand_direc + probability * pref_direc
        return biased_vec / np.linalg.norm(biased_vec)



    def vec_magnitude (vector : tuple) -> int:
        return np.linalg.norm(vector)
    
    def opposite_direction (vector : tuple) -> tuple:
        return (-vector[0], -vector[1], -vector[2])

    # def update_postion(orig_pos : tuple):
    #     new_x = orig_pos[0] + random.uniform(-1, 1) * config.step
    #     new_y = orig_pos[1] + random.uniform(-1, 1) * config.step
    #     new_z = orig_pos[2] + random.uniform(-1, 1) * config.step
    #     return (new_x, new_y, new_z)
    