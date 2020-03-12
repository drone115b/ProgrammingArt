import art

def voronoishader(x, y):
    c, C = art.voronoinoise2d((x * 16.0, y * 16.0))
    C = art.tilenoise2d(C)
    C = (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)
    C = tuple((1-c)*x for x in C)
    return C

if "__main__" == __name__ :
  art.render(voronoishader, "example_005.png", 256, 196, 4)
