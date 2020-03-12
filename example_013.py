import art

def shader(x, y):
    P = (x*44.0, y*2.0) # high frequency signal
    dP = art.simnoise2d((13.5 + x*1.3,23.5 + y*1.3)) # low frequency signal
    P = art.addV(dP,P) # dP added to P
    c, C = art.voronoinoise2d(P)
    brown1 = (0.5,0.4,0.05)
    brown2 = (0.35,0.27,0.03)
    return art.mixV(brown1, brown2, c)

if "__main__" == __name__ :
  art.render(shader, "example_013.png", 256, 196, 8)
