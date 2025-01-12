"""
File for configuration of the app.
"""

# ARGUMENTS
layout_choices = ["cube", "sphere", "random"]
layout_default = layout_choices[2]
atoms_default = [50]

#COLORS
atom_edge_color = (0.5, 0.5, 0.5, 0.5)
atom_color = {
    -1 : "#87CEEB",
    0 : "#9e0142",
    1 : "#d53e4f",
    2 : "#f46d43",
    3 : "#fdae61",
    4 : "#fee08b",
    5 : "#e6f598",
    6 : "#abdda4",
    7 : "#66c2a5",
    8 : "#3288bd",
    9 : "#5e4fa2",
}

#SIMULATION
step = 0.25
direc_prob = 0.1

# DISPLAY
atom_radius = 0.7