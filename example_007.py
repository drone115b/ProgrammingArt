import art

def simshader(x, y):
    baseP = [x*16.0,y*16.0]
    dP = art.simnoise2d(baseP)
    P = tuple((b*0.35 + a) for a,b in zip(baseP,dP))
    C = art.tilenoise2d(P)
    assert 3 == len(C)
    # remap domain from (-1,1) to (0,1) for output
    return (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)

if "__main__" == __name__ :
  art.render(simshader, "example_007.png", 256, 196, 4)
