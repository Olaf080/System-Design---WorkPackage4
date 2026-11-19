

## Metal -> 0
## Composite -> 1


def Spacing(Mat,DiameterFastener,n):

    if Mat == 0:
        SpaceU = 3 * DiameterFastener
        SpaceL = 2 * DiameterFastener
    elif Mat == 1:
        SpaceU = 5 * DiameterFastener
        SpaceL = 4 * DiameterFastener

    EdgeDistance = 1.5 * DiameterFastener

    i = 1
    while i <= n:
        WConservative = SpaceL * (i-1) + 2  *EdgeDistance
        WRisky = SpaceU * (i-1) + 2 * EdgeDistance
        print(WConservative,WRisky)
        i += 1

print(Spacing(1,2,4))