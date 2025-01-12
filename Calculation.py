import config
import numpy as np


class Calculation ():
    """
    This class manage all calculations of the simulation.

    Attributtes:
        master (Simulation): Parent of the Calculation (parent simulation).
        ions (list): list of all ions in simulation
        electrodes (list): list of all electrodes in simulation
    """
    def __init__(self, master) -> None:
        """
        Initialize calculation.

        Args:
            master (Simulation): parent simulation
        """
        self.master = master
        self.ions = master.ions
        self.electrodes = master.electrodes

    def calculate_sim (self) -> None:
        """
        Performs all steps of the simulation until all ions becoma eletrodes.

        Performs next step of the simulationif there are at least one free particle in space, otherwise calculation (and whole simulation) is terminated.
        """
        while len(self.ions) != 0:
            for ion in self.ions:
                shoretes_dist, nearest_elec = self._shortest_electrode_dist(ion)
                if (self._is_electrode(ion, nearest_elec)):
                    continue
                ion.electrode_dist = shoretes_dist
                shift_vec = self._gen_biased_vector(ion, nearest_elec)
                ion.update_position(ion.position + shift_vec * config.step)
            
    def _is_electrode (self, ion, nearest_electrode) -> bool:
        """
        Check if is free ion is near to some electrode and return bool. If true, transform atom (ion) attributtes to an electrode configuration and reassign to the electrone group.

        Args:
            ion (Atom): Atom of interest
            nearest_electrode (Atom): Nearest electrode to the Atom of interest

        Return:
            bool: If the ion nedd tradform to the electrode
        """
        if (ion.electrode_dist <= config.atom_radius*2 + config.step/2):
            ion.transform_to_electrode(nearest_electrode)
            self.electrodes.append(ion)
            self.ions.remove(ion)
            return True
        return False

    def _shortest_electrode_dist(self, ion):
        """
        Calculate amgnitude of the distance from ion the the nearest electrode of dendrimer.

        Args:
            ion (Atom): Atom of interest

        Returns:
            float: shortest distance the (nearsert) electrode
            Atom: nearest electrod
        """
        shortest_dist = 1000
        nearest_elec = self.master.electrode
        for electrode in self.electrodes:
            actual_distance = np.linalg.norm(ion.position - electrode.position)
            if (actual_distance < shortest_dist):
                shortest_dist = actual_distance
                nearest_elec = electrode
        return shortest_dist, nearest_elec

    def _gen_biased_vector (self, ion, nearest_electrode) -> np.array:
        """
        Calculate a vector of motion of the atom.

        Sums prefered vector (from ion the nearest electrode, weighted by probability from config file) with random generated vector (weighted by (1 - probability) from config file) and normalized it.

        Args:
            ion (Atom): Atom of interest
            nearest_electrode (Atom): Nearest electrode of dendrimer

        Returns:
            np.array: Vector of the motion of the atom
        """
        probability = config.direc_prob
        pref_direc = nearest_electrode.position - ion.position
        pref_direc = pref_direc / np.linalg.norm(pref_direc)
        rand_direc = np.random.randn(3)
        rand_direc = rand_direc / np.linalg.norm(rand_direc)
        biased_vec = (1 - probability) * rand_direc + probability * pref_direc
        return np.array(biased_vec / np.linalg.norm(biased_vec))
    
    def final_pos_optimalization (atom) -> np.array:
        """
        Optimize a particle position when the ion os boud to the dendrimer and stops motion.

        Args:
            atom (Atom): Atom of interest

        Returns:
            np.array: new (adjusted) positon of the atom in the space
        """
        electrode_pos = atom.parent_electrode.position
        elec_to_ion = np.array(atom.position - electrode_pos)
        distance = np.linalg.norm(elec_to_ion)
        if (distance == 0):
            return np.array(atom.position)
        norm_elec_to_ion = np.array(elec_to_ion / distance)
        return np.array(electrode_pos + norm_elec_to_ion * 2 * config.atom_radius)


    def vec_magnitude (vector : np.array) -> float:
        """
        Return magnitude of the vector.

        Args:
            vector (np.array): vector

        Returns:
            float: magnitude of the vector
        """
        return np.linalg.norm(vector)
    
    def opposite_direction (vector : np.array) -> np.array:
        """
        Return opposite direction of the vector in 3D.

        Args:
            vector (np.array): vector

        Returns:
            np.array: vector with opposite direction
        """
        return (-vector[0], -vector[1], -vector[2])
    