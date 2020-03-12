import art

def voronoishader(x, y):
    c, C = art.voronoinoise2d((x * 16.0, y * 16.0))
    C = art.tilenoise2d(C)
    # remap domain from (-1,1) to (0,1) for output
    return (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)
    
if "__main__" == __name__ :
  art.render(voronoishader, "example_004.png", 256, 196, 4)
