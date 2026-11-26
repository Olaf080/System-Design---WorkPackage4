import numpy as np 
import math
import matplotlib.pyplot as plt
from itertools import product
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import brentq

#2024-T4 Plate
D_2 = 0.004
maxSC = 760 * 1e6
maxWall = 441 * 1e6

t_list = np.arange(0.001, 0.051, 0.001)



def BearFail(D2, t_2, maxPart):
        sigma_br = 11671.655/(D2 * t_2)
        if sigma_br >= maxPart:
            return False
        return True

for i in t_list:
    if BearFail(D_2, i, maxWall):
        print(i)
        break


