
import sys
from pathlib import Path

spacing_folder = Path(__file__).resolve().parent.parent / "4.4-Fastener Spacing"
sys.path.append(str(spacing_folder))
from FastenerPattern import Spacing


F_cgx = 582.67
F_cgy = 299.66 
F_cgz = 299.66

n = 6

''' 

Assuming that the Fastener Configuration is symmetric around the x,z-axis
We find that :
  F_cgx = F_x
  F_cgz = F_z 

'''

Fx = F_cgx / n
Fz = F_cgz / n

# Bearing Stress is the stress between the fastener and the material it is put in
