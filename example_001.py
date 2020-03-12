import art

def tileshader(x, y):
    C = art.tilenoise2d((x * 16.0, y * 16.0))
    assert 3 == len(C)
    # remap domain from (-1,1) to (0,1) for output
    return (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)


if "__main__" == __name__ :
  art.render(tileshader, "example_001.png", 256, 196, 4)
