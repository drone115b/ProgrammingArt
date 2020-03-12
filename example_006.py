import art

def simshader(x, y):
    C = art.simnoise3d((x * 16.0, y * 16.0, 0.5))
    return (C[0]*0.5 + 0.5, C[1]*0.5 + 0.5, C[2]*0.5 + 0.5)

if "__main__" == __name__ :
  art.render(simshader, "example_006.png", 256, 196, 4)
