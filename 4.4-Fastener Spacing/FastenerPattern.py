

## Metal -> 0
## Composite -> 1
x_cords = []
z_cords = []

def Spacing(Mat,DiameterFastener,conservative,n,x_cords,z_cords,t_1):

    if Mat == 0:
        if conservative ==0:
            Space = 2 * DiameterFastener
        else:
            Space = 3 * DiameterFastener
    elif Mat == 1:
        if conservative ==0:
            Space = 5 * DiameterFastener
        else:
            Space = 4 * DiameterFastener

    EdgeDistance = 1.5 * DiameterFastener

    W = Space * (n-1) + 2  *EdgeDistance
    print(W)
    i=n

    
    while i>0:
        #left side
        x_cords.append(-(t_1/2+ 1.5*DiameterFastener+0.5*DiameterFastener))
        z_cords.append((i-1/2)*DiameterFastener+1.5*DiameterFastener+(Space-1)*(i-1)-(n*DiameterFastener+3*DiameterFastener+(Space-1)*(n-1))/2)
        #right side
        x_cords.append(t_1/2+ 1.5*DiameterFastener+0.5*DiameterFastener)
        z_cords.append((i-1/2)*DiameterFastener+1.5*DiameterFastener+(Space-1)*(i-1)-(n*DiameterFastener+3*DiameterFastener+(Space-1)*(n-1))/2)
        i=i-1
    print(x_cords,z_cords)

    x_sum=0 
    z_sum = 0
    x_cg = 0
    z_cg= 0
    for i in range(0,2*n):
        x_sum += x_cords[i]
        z_sum += z_cords[i]
        x_cg = x_sum/n
        z_cg=z_sum/n
    print(x_cg,z_cg)


print(Spacing(1,2,0,4,x_cords,z_cords,1))