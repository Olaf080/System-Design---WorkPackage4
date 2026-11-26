import math
import sys
from pathlib import Path

# Import Spacing from the neighbouring 4.4 folder
project_folder = Path(__file__).resolve().parent.parent
spacing_folder = project_folder / "4.4-Fastener Spacing"
sys.path.insert(0, str(spacing_folder))

from FastenerPattern import Spacing

M_z = 439500 #N mm



def calc_r (x_cords, y_cords, x_cg, y_cg):
    r=[]

    for x_ij, y_ij in zip(x_cords, y_cords):
        r_ij = math.sqrt((x_ij-x_cg)**2 + (y_ij - y_cg)**2)
        r.append(r_ij)

    return r


def calc_moment(x_cords, y_cords, x, y):
    Fy = 1098.7
    Fx = 329.6

    n = len(x_cords)
    x_cg = sum(x_cords) / n  
    y_cg = sum(y_cords) / n
    
    M_zcg =  Fy*(x-x_cg) - Fx*(y-y_cg) + M_z

    r = calc_r(x_cords, y_cords, x_cg, y_cg)
    J = sum(r_ij**2 for r_ij in r)

    # Calculate individual fastener forces
    F = []

    for r_ij in r:
        F_ij = abs(M_zcg) * r_ij / J
        F.append(F_ij)

    return F

x_cords = []
y_cords = []

Spacing(0, 4, 0, x_cords, y_cords, 1, 2, 1)

#force centred at the centre of the plate
F = calc_moment (x_cords, y_cords, x=0, y=0)
print(x_cords)
print(y_cords)
print(F)




