import art

def distanceonly(P):
    c, C = art.voronoinoise2d(P)
    return (c,c,c)

def shader(x, y):
    P = (x, y)
    c = art.fractalV(P, distanceonly, 8.0, 2)[0]
    C0 = (1.0,0.1,0.1) # red
    C1 = (0.91,0.9,0.8) # white
    C2 = (0.15,0.12,0.08)
    C = tuple(art.spline(c,*args) for args in zip(C0,C1,C2))
    return C

if "__main__" == __name__ :
  art.render(shader, "example_014.png", 256, 196, 4)
