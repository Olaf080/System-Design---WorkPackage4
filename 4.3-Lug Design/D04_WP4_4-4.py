import math
import matplotlib.pyplot as plt
import numpy as np 
from itertools import product
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import brentq

Axial = 299.66/2
Trans = 998.85/2
SafetyMarg = 0.5

def MaxHoleStress(F_a, F_t, F_x, W, D, t):
    #THIS FUNCTION IS AI- REQUIRES SOLVING 10TH ROOTS

    A = abs(F_a) / t
    B = 6 * abs(F_t) * W / t
    C = 6 * abs(F_x) / t**2

    # Width of hole at section y
    def d(y):
        return np.sqrt(np.maximum(0, D**2 - 4*y**2))

    # Combined axial and bending stress
    def Stress(y):
        h = d(y)

        return (
            (A + C*y) / (W - h)
            + B*y / (W**3 - h**3)
        )

    # Simplified stationary-point equation
    def Stationary(y):
        h = d(y)

        return (
            C*(W*h - D**2)
            - 4*A*y
            + B*h*(W**3 + 2*h**3 - 3*D**2*h)
            / (W**2 + W*h + h**2)**2
        )

    # Include boundaries as possible maxima
    candidates = [0, D/2]

    # Search for stationary points
    y_vals = np.linspace(0, D/2, 200)
    derivatives = Stationary(y_vals)

    for i in range(len(y_vals) - 1):

        if derivatives[i] == 0:
            candidates.append(y_vals[i])

        elif derivatives[i]*derivatives[i+1] < 0:
            y_stationary = brentq(
                Stationary,
                y_vals[i],
                y_vals[i+1]
            )

            candidates.append(y_stationary)

    # Find the location giving the highest stress
    stresses = Stress(np.array(candidates))
    index = np.argmax(stresses)

    return stresses[index], candidates[index]





def FailChecker(F_a, F_t, W, D, t, Fam, MSafety, L):
    F_x = 299.66/2
    if D>= W:
        return False
    Tempy = [0, 6, 9, 11]
    if Fam == 0:
        Mat = 0
    else:
        for i in range(0, 3):
                if Tempy[i] < Fam <= Tempy[i + 1]:
                    Mat = i
                    break

    FtUlt = [448, 686, 620, 540, 434, 540, 490, 475.74, 475.74, 468.84, 275.10, 206.84]
    Ft_Yield = [386, 210, 550, 485, 510, 480, 420, 310.26, 324.05, 324.05, 144.79, 137.90]
    G12_Curves = np.array([[1, 0.99, 0.97, 0.94, 0.92, 0.92, 0.89, 0.85, 0.76],  [1, 0.96, 0.9, 0.84, 0.8, 0.76, 0.74, 0.72, 0.68], [0.68, 0.63, 0.58, 0.54, 0.5, 0.46, 0.43, 0.38, 0.34]])


    G14_Curves = np.array([[0, 0.63, 0.86, 0.95, 0.98, 0.999, 1, 1], [0, 0.79, 0.99, 1.07, 1.11, 1.12, 1.13, 1.13], [0, 0.82, 1.08, 1.17, 1.21, 1.23, 1.24, 1.24], [0,0.9,1.12,1.23,1.29,1.3,1.3,1.3], [0,0.9,1.2,1.31,1.37,1.4,1.41,1.41], [0,0.9,1.29,1.41,1.47,1.5,1.5,1.5], [0,0.9,1.35,1.5,1.6,1.61,1.62,1.62], [0,0.9,1.35,1.55,1.65,1.69,1.7,1.7], [0,0.9,1.35,1.6,1.7,1.72,1.75,1.75]])
    G14_alts = [0.06, 0.08, 0.1, 0.12, 0.15, 0.2, 0.3, 0.4, 0.6]
    G15_Curves = [0, 0.25, 0.45, 0.72, 0.88, 1.04, 1.16, 1.29]

    r1 = W/D
    if r1 > 5 or r1 < 1:
        return False
    r2 = t/D
    if r2 < 0.06:
        return False
    r3 = r1/2
    if r3 < 0.5 or r3 > 4:
        return False
    
    A_1 = ((W/2) - (D/2)/math.sqrt(2)) * t
    A_2 = ((W/2) - (D/2))*t
    A_avg = 6 / ((4/A_1) + (2/A_2))
    A_br = D * t
    r4 = A_avg / A_br
    if r4 > 1.4:
        return False


    #Check Root Bending
    sigma_root = F_a/(W*t) + 6*(L + (W/2)) * ((F_x/(W * (t**2))) + (F_t/(t * (W ** 2))))
    if (1 + MSafety) * sigma_root >= Ft_Yield[Fam] * 1e6:
        return False


    sigma_max, y_max = MaxHoleStress(
        F_a, F_t, F_x, W, D, t
    )

    if (1 + MSafety)*sigma_max >= Ft_Yield[Fam]*1e6:
        return False



    #Checking Eq6

    r1_floor = (0.5 * math.floor(r1/0.5))
    K_t = np.interp(r1, np.linspace(1, 5, 9), G12_Curves[Mat])
    P6 = K_t * Ft_Yield[Fam] * (W - D)* t * 1000000

    #Checking Eq8
    r3_floor = (0.5 * math.floor(r3/0.5))
    if r2 >= 0.6:
        Corr_Val = 8
    else:
        for i in range(0, 8):
            if G14_alts[i] <= r2 < G14_alts[i + 1]:
                Corr_Val = i
                break
    K_bry = np.interp(r3, np.linspace(0.5, 4, 8), G14_Curves[Corr_Val])
    P8 = K_bry * Ft_Yield[Fam] * A_br * 1000000

    #Finding R_a
    R_a = F_a / min(P6, P8)

    #Checking Eq11
    r4_floor = (0.2 * math.floor(r4/0.2))
    K_ty = np.interp(r4, np.linspace(0, 1.4, 8), G15_Curves)
    P11 = K_ty * A_br * Ft_Yield[Fam]* 1000000

    #Finding R_t
    R_t = F_t / P11

    Result = (R_a ** 1.6) + (R_t**1.6)

    if ((1/(Result ** 0.625)) - 1) <= MSafety:
        return False
    else:
        return True

W_vals = np.arange(0.0201, 0.1, 0.001)
L_vals = [0.02]
t_vals = np.arange(0.001, 0.051, 0.001)
Mat_vals = np.arange(0, 12)



Final = 100000000000
Result = [1, 3, 5, 4]
for i, k, l, j in product(W_vals, t_vals, Mat_vals, L_vals):
        if FailChecker(Axial, Trans, i, 0.02, k, l, SafetyMarg, j):
            Vol = (k * ((i**2)*((1/2) + (math.pi/8)) - (0.02**2)*(math.pi/4) + i*j))
            if l ==0 or l == 3 or l == 6:
                Weight = Vol * 2810
            elif l ==7 or l == 8 or l == 9:
                Weight = Vol * 2780
            elif l == 1 or l == 2:
                Weight = Vol * 7850
            elif l == 10:
                Weight = Vol * 1810
            elif l == 11:
                Weight = Vol * 2680
            if Weight <= Final:
                Final = Weight
                Result = [i, k, l, j]

print("Width is ", Result[0])
print("Thickness is ", Result[1])
print("Material is ", Result[2])
print("Length is ", Result[3])


sigma_max, y_max = MaxHoleStress(
    Axial, Trans, 299.66/2,
    Result[0], 0.02, Result[1]
)

print("Maximum hole stress:", sigma_max/1e6, "MPa")
print("Location from hole centre:", y_max*1000, "mm")

