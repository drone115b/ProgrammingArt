import art

def voronoishader(x, y):
    c, C = art.voronoinoise2d((x * 16.0, y * 16.0))
    return (c,c,c)

if "__main__" == __name__ :
  art.render(voronoishader, "example_003.png", 256, 196, 4)
