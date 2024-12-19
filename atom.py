from vispy import scene
from vispy.visuals.transforms import STTransform


from Calculation import Calculation
import config


class Atom ():
    def __init__(self, type : str, position : tuple):
        self.type = type
        self.position = position
        self.positions_list = [self.position]
        self.freeze = self._set_freeze()
        self.freeze_distance = Calculation.vec_magnitude(Calculation.opposite_direction(self.position))
        self.color = self._set_fg_color()

    def _set_fg_color (self):
        if (self.type == "ion"):
            return config.ion_color
        return config.electrode_color
    
    def _set_freeze (self):
        if (self.type == 'ion'):
            return False
        return True
        
    def display(self, view, time : str) -> None:
        self.sphere = scene.visuals.Sphere(radius=1, method='ico', parent=view.scene, color = self.color, edge_color = config.atom_edge_color)
        position = self.positions_list[0] if time == "start" else self.positions_list[-1]
        self.translate(position)

    # def update(self, view) -> None:
    #     self.x_pos, self.y_pos, self.z_pos = Calculation.update_postion((self.x_pos, self.y_pos, self.z_pos))
    #     self.translate()

    def update_position(self, new_position : tuple) -> None:
        self.position = new_position
        self.positions_list.append(new_position)

    def translate (self, pos : tuple) -> None:
        self.sphere.transform = STTransform(translate=[pos[0], pos[1], pos[2]])

    def reduce_freeze_dist (self) -> None:
        self.freeze_distance -= 2*config.step