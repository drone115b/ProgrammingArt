from . import hash
import math

#########

def L1distanceV(P0, P1):
  "Manhattan distance between two vectors (2d or 3d)"
  return sum(abs(a-b) for a,b in zip(P0,P1))

def L2distanceV(P0, P1):
  "Euclidean distance between two vectors (2d or 3d)"
  return sum((a-b)*(a-b) for a,b in zip(P0,P1)) ** 0.5

#########

def smoothstepCubic(x):
  "C2-Smooth transition from zero to one, given an input in the range(0,1)"
  return x * x * (3 - 2 * x)

def smoothstepCubicV(P):
  "C2-Smooth transition from zero to one, applied to each component of a vector"
  return tuple(smoothstepCubic(x) for x in P)

def smoothstep(x):
  "C4-Smooth transition from zero to one, given an input in the range(0,1)"
  return (x * x * x) * ( 10.0 + x * ( 6.0 * x - 15.0 ))

def smoothstepV(P):
  "C4-Smooth transition from zero to one, applied to each component of a vector"
  return tuple(smoothstep(x) for x in P)

def bell( x ):
  "Smooth bell, value zero for input 0 or 1, max value at input = 0.5"
  return (16.0 * x * x) * ( 1.0 + x * ( x - 2.0 ))

def bellV( P ):
  "Smooth bell, value zero for input 0 or 1, max value at input = 0.5; applied to each component of a vector"
  return tuple(bell(x) for x in P)

def clamp(x):
  "Given a value, returns zero if the value<0, one if value>1 otherwise the value itself"
  return min(1.0,max(0.0,x))

def clampV(Pa, Pb, x):
  "Restricts each component of a vector to range(0,1)"
  return tuple(mix(a,b,x) for a,b in zip(Pa,Pb))

def mix( a, b, x ):
  "Linear mix: returns a for x=0, b for x=1 or linear blend for x in the range(0,1)"
  return a + (b-a)*clamp(x)

def mixV( Pa, Pb, x ):
  "Linear blend of each component of input vectors"
  return tuple(mix(a,b,x) for a,b in zip(Pa,Pb))

def addV(Pa, Pb):
  "Returns a vector whose components are the sum of the components from the inputs"
  return tuple(a+b for a,b in zip(Pa,Pb))

def subV(Pa, Pb):
  "Returns a vector whose components are the difference of the components from the inputs"
  return tuple(a-b for a,b in zip(Pa,Pb))

def mulV(Pa, Pb):
  "Returns a vector whose components are the product of the components from the inputs"
  return tuple(a*b for a,b in zip(Pa,Pb))

def spline(x, *args):
    "Interpolates the arguments, varying across them as input varies from zero to one"
    def get_v_dv(i, a):
        v = None
        if i <= 0:
            lo = a[0]
            v = a[0]
        else:
            lo = a[i-1]
        if i >= len(a)-1:
            hi = a[-1]
            v = a[-1]
        else:
            hi = a[i+1]
        if v is None:
            v = a[i]
        return v, hi-lo

    y = x*len(args)
    yi = math.floor(y)
    v0, dv0 = get_v_dv(int(yi),args)
    v1, dv1 = get_v_dv(int(yi)+1,args)
    y = y - yi

    y2 = y*y
    y3 = y2*y

    return (
       (2.0*y3 - 3.0*y2 + 1.0) * v0 +
       (y3 + y2*-2.0 + y) * dv0 +
       (-2.0*y3 + 3.0*y3) * v1 +
       (y3 - y2) * dv1
    )

#########

def tilenoise2d(P):
  "Constant value returned for each lattice; return triple in range +/- 1"
  P00 = (math.floor(P[0]), math.floor(P[1]))
  h0 = float(hash.hash16b3d(int(P00[0]), int(P00[1]), 11)) * (1.0/(2.0 ** 16))
  h1 = float(hash.hash16b3d(int(P00[0]), int(P00[1]), 22)) * (1.0/(2.0 ** 16))
  h2 = float(hash.hash16b3d(int(P00[0]), int(P00[1]), 33)) * (1.0/(2.0 ** 16))
  return (2*h0-1, 2*h1-1, 2*h2-1)


def tilenoise3d(C):
  "Constant value returned for each lattice; return triple in range +/- 1"
  C00 = (int(math.floor(C[0])), int(math.floor(C[1])), int(math.floor(C[2])))
  h0 = float(hash.hash16b3d(C00[0], C00[1], C00[2] ^ 0x36)) * (1.0/(2.0 ** 16))
  h1 = float(hash.hash16b3d(C00[1], C00[2], C00[0] ^ 0x75)) * (1.0/(2.0 ** 16))
  h2 = float(hash.hash16b3d(C00[2], C00[0], C00[1] ^ 0x91)) * (1.0/(2.0 ** 16))
  return (2.0*h0-1.0, 2.0*h1-1.0, 2.0*h2-1.0)

#########

def valuenoise1d(x, seed=0):
  "Smooth blended value returned for each lattice; returns range +/- 1, 3d tuple"
  i = math.floor(x)
  ret = []
  for j in range(3):
    h0 = float(hash.hash16b3d(int(i), int(j), seed)) * (2.0 ** -16)
    h1 = float(hash.hash16b3d(int(i+1), int(j), seed)) * (2.0 ** -16)
    ret.append(2.0 * mix(h0, h1, smoothstepCubic(x-i)) - 1.0)
  return tuple(ret)


def valuenoise2d(P):
  "Smooth blended value returned for each lattice; returns range +/- 1, 3d tuple"
  C00 = tilenoise2d((P[0], P[1]))
  C01 = tilenoise2d((P[0], P[1]+1.0))
  C10 = tilenoise2d((P[0]+1.0, P[1]))
  C11 = tilenoise2d((P[0]+1.0, P[1]+1.0))
  x = P[0] - math.floor(P[0])
  y = P[1] - math.floor(P[1])
  return mixV(
      mixV(C00, C10, smoothstepCubic(x)),
      mixV(C01, C11, smoothstepCubic(x)),
    smoothstepCubic(y)
  )

def valuenoise3d(P):
  "Smooth blended value returned for each lattice; returns range +/- 1, 3d tuple"
  C000 = tilenoise3d((P[0], P[1], P[2]))
  C010 = tilenoise3d((P[0], P[1]+1.0, P[2]))
  C100 = tilenoise3d((P[0]+1.0, P[1], P[2]))
  C110 = tilenoise3d((P[0]+1.0, P[1]+1.0, P[2]))
  C001 = tilenoise3d((P[0], P[1], P[2]+1.0))
  C011 = tilenoise3d((P[0], P[1]+1.0, P[2]+1.0))
  C101 = tilenoise3d((P[0]+1.0, P[1], P[2]+1.0))
  C111 = tilenoise3d((P[0]+1.0, P[1]+1.0, P[2]+1.0))
  x = P[0] - math.floor(P[0])
  y = P[1] - math.floor(P[1])
  z = P[2] - math.floor(P[2])

  R00 = mixV(C000, C100, smoothstepCubic(x))
  R01 = mixV(C001, C101, smoothstepCubic(x))
  R10 = mixV(C010, C110, smoothstepCubic(x))
  R11 = mixV(C011, C111, smoothstepCubic(x))
  R0 = mixV(R00, R10, smoothstepCubic(y))
  R1 = mixV(R01, R11, smoothstepCubic(y))
  return mixV(R0, R1, smoothstepCubic(z))

#########

def voronoinoise2d(P, distancefn=L2distanceV):
    "Returns distance (scalar), position (2d)"
    dist = 100.0
    retP = P
    for i in range(-1,2):
        for j in range(-1,2):
            dP = tilenoise2d((P[0]+i,P[1]+j))
            dP = (0.5 * dP[0] + 0.5, 0.5 * dP[1] + 0.5) # range 0-1
            dP = (dP[0]*0.9 + 0.05, dP[0]*0.9 + 0.05) # range 0.05 to 0.95
            cmpP = (dP[0]+math.floor(P[0])+i, dP[1]+math.floor(P[1])+j) # hashed position
            d = distancefn(P,cmpP)
            if d < dist:
                retP = cmpP
                dist = d
    return dist, retP


def voronoinoise3d(P, distancefn=L2distanceV):
    "Returns distance (scalar), position (3d)"
    dist = 100.0
    retP = P
    for i in range(-1,2):
        for j in range(-1,2):
            for k in range(-1,2):
                dP = tilenoise3d((P[0]+i,P[1]+j,P[2]+k))
                dP = (0.5 * dP[0] + 0.5, 0.5 * dP[1] + 0.5, 0.5 * dP[2] + 0.5) # range 0-1
                dP = (dP[0]*0.9 + 0.05, dP[1]*0.9 + 0.05, dP[2]*0.9 + 0.05) # range 0.05 to 0.95
                cmpP = (dP[0]+math.floor(P[0])+i, dP[1]+math.floor(P[1])+j, dP[2]+math.floor(P[2])+k) # hashed position
                d = distancefn(P,cmpP)
                if d < dist:
                    retP = cmpP
                    dist = d
    return dist, retP


#########

def simnoise3d(P):
  "Returns a 3d motion vector; each component in range(-1,1)"
  Pi = [0] * 3
  Pt = [0] * 3
  b = [0] * 3
  for i in range(3):
      Pi[i] = int(math.floor(P[i]))
      Pt[i] = P[i] - Pi[i]
      b[i] = bell( Pt[i] )

  corner = [(0,0,0)] * 7
  for i in range(7):
    Pi[0] += i & 0x01
    Pi[1] += (i>>1) & 0x01
    Pi[2] += (i>>2) & 0x01

    # this can be a hash, for a 3d input vector;
    # or a 1d noise for 4d position + time input vector
    corner[i] = tilenoise3d(Pi)

    Pi[0] -= i & 0x01
    Pi[1] -= (i>>1) & 0x01
    Pi[2] -= (i>>2) & 0x01

  face = [0] * 6
  face[0] = ( corner[4][1] - corner[0][1] ) + ( corner[0][2] - corner[2][2] )
  face[1] = ( corner[5][1] - corner[1][1] ) + ( corner[1][2] - corner[3][2] )
  face[2] = ( corner[4][0] - corner[0][0] ) + ( corner[1][2] - corner[0][2] )
  face[3] = ( corner[6][0] - corner[2][0] ) + ( corner[3][2] - corner[2][2] )
  face[4] = ( corner[0][1] - corner[1][1] ) + ( corner[0][0] - corner[2][0] )
  face[5] = ( corner[4][1] - corner[5][1] ) + ( corner[4][0] - corner[6][0] )

  return(
         b[1] * b[2] * mix( face[0], face[1], smoothstep(Pt[0]) ),
         b[0] * b[2] * mix( face[2], face[3], smoothstep(Pt[1]) ),
         b[0] * b[1] * mix( face[4], face[5], smoothstep(Pt[2]) )
  )


def simnoise2d(P):
  "Returns a 2d motion vector; each component in range(-1,1)"
  Pi = [0] * 2
  Pt = [0] * 2
  b = [0] * 2
  for i in range(2):
      Pi[i] = int(math.floor(P[i]))
      Pt[i] = P[i] - Pi[i]
      b[i] = bell( Pt[i] )

  corner = [0] * 4
  for i in range(4):
    Pi[0] += i & 0x01
    Pi[1] += (i>>1) & 0x01

    # this can be a hash, for a 3d input vector;
    # or a 1d noise for 4d position + time input vector
    corner[i] = tilenoise2d(Pi)[0]

    Pi[0] -= i & 0x01
    Pi[1] -= (i>>1) & 0x01

  return(
         b[1] * mix( corner[0] - corner[2], corner[1] - corner[3], smoothstep(Pt[0]) ),
         b[0] * mix( corner[1] - corner[0], corner[3] - corner[2], smoothstep(Pt[1]) )
  )


#########

def fractal(x, fn, scale, octaves=4, lac=1.7, dim=1.0/1.7):
    """"Given a scalar value, a function of a scalar value, and the scale of the detail;
    and optionally, a number of octaves, lacunarity (float>1) and dimension(float<1),
    returns a fractal summation of the signal
    """
    V = x * scale
    amt = None
    assert(octaves>=1)
    for i in range(octaves):
        val = fn(V)
        V = V*lac
        if amt is None:
            ret = val
            norm = 1
            amt = dim
        else:
            ret += val * amt
            norm += amt
            amt *= dim
    return ret / norm


def fractalV(P, fn, scale, octaves=4, lac=1.7, dim=1.0/1.7):
    """"Given a position, a multi-dimensional noise function, and the scale of the detail;
    and optionally, a number of octaves, lacunarity (float>1) and dimension(float<1),
    returns a fractal summation of the signal
    """
    V = tuple(x * scale for x in P)
    amt = None
    assert(octaves>=1)
    for i in range(octaves):
        val = fn(V)
        V = tuple(x*lac for x in V)
        if amt is None:
            ret = val
            norm = 1
            amt = [dim] * len(val)
        else:
            ret = addV(ret, mulV(val, amt))
            norm += amt[0]
            amt = mulV(amt, [dim] * len(amt))
    return mulV(ret, [1.0/norm] * len(ret))
