import art

def noiseshader(x, y):
    C = art.valuenoise2d((x * 16.0, y * 16.0))
    assert 3 == len(C)
    # remap domain from (-1,1) to (0,1) for output
    return (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)


if "__main__" == __name__ :
  art.render(noiseshader, "example_002.png", 256, 196, 4)
