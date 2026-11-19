import math

# n = columns
# m = rows
# total number of fastners = n * m 
# i,j matrix position
# Fx, Fy - forces


r=[]

def calc_r (n, m, g, Space, EdgeDistance):
    for i in range(1, n+1):
        for j in range(1, m+1):
            x_ij = g/2 + (i-1)*Space
            z_ij = (j-(m+1)/2)*Space

            r_ij = math.sqrt(x_ij**2 + z_ij**2)

            r.append(r_ij)
            r.append(r_ij) #add a second time because there are fastners on both sides

    return r


def calc_moment(n, m, g, Space, x, z):
    Fz = 582.67*1.5
    Fx = 299.66*1.5

    #centroid (dummy values)
    x_cg = 0
    z_cg = 0 
    
    M_ycg = - Fz*(x-x_cg) + Fx*(z-z_cg)

    r = calc_r(n, m, g, Space)
    J = sum(r_ij**2 for r_ij in r)

    # Calculate individual fastener forces
    F = []

    for r_ij in r:
        F_ij = abs(M_ycg) * r_ij / J
        F.append(F_ij)

    return F




