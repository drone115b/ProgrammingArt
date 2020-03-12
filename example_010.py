import art

def shader(x, y):
    P = (x*16.0, y*16.0)
    c, C = art.voronoinoise2d(P, art.L1distanceV)
    return (c,c,c)

if "__main__" == __name__ :
  art.render(shader, "example_010.png", 256, 196, 4)
