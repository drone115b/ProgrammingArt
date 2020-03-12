import art

def distance(A,B):
    return max(abs(a-b) for a,b in zip(A,B))

def shader(x, y):
    P = (x*16.0, y*16.0)
    c, C = art.voronoinoise2d(P, distance)
    return (c,c,c)

if "__main__" == __name__ :
  art.render(shader, "example_011.png", 256, 196, 4)
