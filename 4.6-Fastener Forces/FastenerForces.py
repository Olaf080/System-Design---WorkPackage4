
import math 
import sys
from pathlib import Path

spacing_folder = Path(__file__).resolve().parent.parent / "4.4-Fastener Spacing"
sys.path.append(str(spacing_folder))
from FastenerPattern import Spacing


F_cgx = 1098.7
F_cgy = 329.6 
F_cgz = 329.6
n = 4

'''
Assuming that the Fastener Configuration is symmetric around the x,z-axis
We find that :
  F_cgx = F_x
  F_cgz = F_z 
'''

#P = math.sqrt(F_cgx**2 + F_cgz**2)/n 
Fx = F_cgx / n
Fz = F_cgz / n
print("Fx is ", Fx)
print("Fz is ", Fz)
#print(Spacing(1,1,1,1,1,1,1,1))
# Bearing Stress is the stress between the fastener and the material it is put in
