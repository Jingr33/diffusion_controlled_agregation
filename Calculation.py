import random
import config


class Calculation ():
    def update_postion(orig_pos : tuple):
        new_x = orig_pos[0] + random.uniform(-1, 1) * config.step
        new_y = orig_pos[1] + random.uniform(-1, 1) * config.step
        new_z = orig_pos[2] + random.uniform(-1, 1) * config.step
        return (new_x, new_y, new_z)