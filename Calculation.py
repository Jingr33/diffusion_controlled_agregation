import random
import config
import numpy as np
from tqdm import tqdm


class Calculation ():
    def __init__(self, master):
        self.master = master
        self.ions = master.ions
        self.electrodes = master.electrodes

    def calculate_sim (self):
        while len(self.ions) != 0:
            for ion in self.ions:
                shoretes_dist, nearest_elec = self._shortest_electrode_dist(ion)
                if (self._is_electrode(ion, nearest_elec)):
                    continue
                ion.electrode_dist = shoretes_dist
                shift_vec = self._gen_biased_vector(ion, nearest_elec)
                ion.update_position(ion.position + shift_vec * config.step)
            
    def _is_electrode (self, ion, nearest_electrode) -> bool:
        if (ion.electrode_dist <= config.atom_radius*2):
            ion.transform_to_electrode(nearest_electrode)
            self.electrodes.append(ion)
            self.ions.remove(ion)
            return True
        return False

    def _shortest_electrode_dist(self, ion):
        shortest_dist = 1000
        nearest_elec = self.master.electrode
        for electrode in self.electrodes:
            actual_distance = np.linalg.norm(ion.position - electrode.position)
            if (actual_distance < shortest_dist):
                shortest_dist = actual_distance
                nearest_elec = electrode
        return shortest_dist, nearest_elec

    def _gen_biased_vector (self, ion, nearest_electrode) -> np.array:
        probability = config.direc_prob
        pref_direc = nearest_electrode.position - ion.position
        pref_direc = pref_direc / np.linalg.norm(pref_direc)
        rand_direc = np.random.randn(3)
        rand_direc = rand_direc / np.linalg.norm(rand_direc)
        biased_vec = (1 - probability) * rand_direc + probability * pref_direc
        return np.array(biased_vec / np.linalg.norm(biased_vec))

    def vec_magnitude (vector : np.array) -> float:
        return np.linalg.norm(vector)
    
    def opposite_direction (vector : np.array) -> np.array:
        return (-vector[0], -vector[1], -vector[2])
    