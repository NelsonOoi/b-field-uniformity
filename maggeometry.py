import numpy as np
import magpylib as magpy
from magpylib.magnet import Cuboid, Cylinder, CylinderSegment
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# define geometry with cylinders along circumference
# used in Ruster and Malinowski
def cyl_ring(n_magnets, br, c_diameter, c_height, st_rad, dist, show=False):
    
    magnets = magpy.Collection()
    theta_range = np.linspace(0, 2*np.pi, n_magnets)
    for theta in theta_range:
        magnets = magnets.add(Cylinder(magnetization=br,
                                     dimension = (c_diameter, c_height),
                                     position = (st_rad * np.cos(theta), st_rad * np.sin(theta), dist)))
    if show:
        magpy.show(magnets, style_magnetization_show=True, backend='plotly')
    return magnets

# define halbach cylinder geometry
def halbach_cylinder(Br, c_d, c_h, D, n, alternate=False):
    magnets = magpy.Collection()
    if alternate:
        n = 2*n
    for i in range(n):
        theta_i = np.radians(720/n * i)
        b_rem = (Br * np.cos(theta_i), Br * np.sin(theta_i), 0)
        pos_ang = np.radians(360/n * i)
        pos = (D/2 * np.cos(pos_ang), D/2 * np.sin(pos_ang), 0)
        src_i = Cylinder(magnetization=b_rem, position=pos, dimension=(c_d, c_h))
        if (i % 2 == 1):
            magnets.add(src_i)
        if (not alternate and i % 2 == 0):
            magnets.add(src_i)
            
    magnets.rotate_from_angax(90, 'x')
    magnets.rotate_from_angax(-90, 'y')
#     magnets.rotate_from_angax(-90, 'z')
    user_defined_style = {
        'show': True,
        "size": 0.1,
        'color': {
            'transition': 0,
            'mode': 'tricolor',
            'middle': 'white',
            'north': 'magenta',
            'south': 'turquoise',
        },
        "mode": "arrow+color",
    }
    magpy.defaults.display.style.magnet.magnetization = user_defined_style
#     magpy.show(magnets, style_magnetization_show=True, backend='plotly')
    return magnets

def four_coils(Br, innerrad1, innerrad2, width, thickness, dist1, dist2, show=False):
    magnets = magpy.Collection()
    ring2_top = CylinderSegment(magnetization=(0, 0, Br),
                               dimension=(innerrad2, innerrad2 + width, thickness, 0, 360),
                               position = (0, 0, +dist2))
    ring1_top = CylinderSegment(magnetization=(0, 0, Br),
                               dimension=(innerrad1, innerrad1 + width, thickness, 0, 360),
                               position = (0, 0, +dist1))
    ring1_bot = CylinderSegment(magnetization=(0, 0, Br),
                               dimension=(innerrad1, innerrad1 + width, thickness, 0, 360),
                               position = (0, 0, -dist1))
    ring2_bot = CylinderSegment(magnetization=(0, 0, Br),
                               dimension=(innerrad2, innerrad2 + width, thickness, 0, 360),
                               position = (0, 0, -dist2))
    magnets.add(ring2_top).add(ring2_bot).add(ring1_top).add(ring1_bot)
    if show:
        magpy.show(magnets, backend='plotly')
    return magnets