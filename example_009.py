import art

def shader(x, y):
    P = (x,y)
    C = art.fractalV(P, art.valuenoise2d, 16.0)
    assert 3 == len(C)
    # remap domain from (-1,1) to (0,1) for output
    return (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)

if "__main__" == __name__ :
  art.render(shader, "example_009.png", 256, 196, 4)
