# Programming Art

A Lunch and Learn for FreshBooks, April 2020

RE: Procedural Texturing in Computer Graphics

## Reference

    L1distanceV(P0, P1)
        Manhattan distance between two vectors (2d or 3d)

    L2distanceV(P0, P1)
        Euclidean distance between two vectors (2d or 3d)

    addV(Pa, Pb)
        Returns a vector whose components are the sum of the components from the inputs

    bell(x)
        Smooth bell, value zero for input 0 or 1, max value at input = 0.5

    bellV(P)
        Smooth bell, value zero for input 0 or 1, max value at input = 0.5; applied to each component of a vector

    clamp(x)
        Given a value, returns zero if the value<0, one if value>1 otherwise the value itself

    clampV(Pa, Pb, x)
        Restricts each component of a vector to range(0,1)

    fractal(x, fn, scale, octaves=4, lac=1.7, dim=0.5882352941176471)
        "Given a scalar value, a function of a scalar value, and the scale of the detail;
        and optionally, a number of octaves, lacunarity (float>1) and dimension(float<1),
        returns a fractal summation of the signal

    fractalV(P, fn, scale, octaves=4, lac=1.7, dim=0.5882352941176471)
        "Given a position, a multi-dimensional noise function, and the scale of the detail;
        and optionally, a number of octaves, lacunarity (float>1) and dimension(float<1),
        returns a fractal summation of the signal

    mix(a, b, x)
        Linear mix: returns a for x=0, b for x=1 or linear blend for x in the range(0,1)

    mixV(Pa, Pb, x)
        Linear blend of each component of input vectors

    mulV(Pa, Pb)
        Returns a vector whose components are the product of the components from the inputs

    simnoise2d(P)
        Returns a 2d motion vector; each component in range(-1,1)

    simnoise3d(P)
        Returns a 3d motion vector; each component in range(-1,1)

    smoothstep(x)
        C4-Smooth transition from zero to one, given an input in the range(0,1)

    smoothstepCubic(x)
        C2-Smooth transition from zero to one, given an input in the range(0,1)

    smoothstepCubicV(P)
        C2-Smooth transition from zero to one, applied to each component of a vector

    smoothstepV(P)
        C4-Smooth transition from zero to one, applied to each component of a vector

    spline(x, *args)
        Interpolates the arguments, varying across them as input varies from zero to one

    subV(Pa, Pb)
        Returns a vector whose components are the difference of the components from the inputs

    tilenoise2d(P)
        Constant value returned for each lattice; return triple in range +/- 1

    tilenoise3d(C)
        Constant value returned for each lattice; return triple in range +/- 1

    valuenoise1d(x, seed=0)
        Smooth blended value returned for each lattice; returns range +/- 1, 3d tuple

    valuenoise2d(P)
        Smooth blended value returned for each lattice; returns range +/- 1, 3d tuple

    valuenoise3d(P)
        Smooth blended value returned for each lattice; returns range +/- 1, 3d tuple

    voronoinoise2d(P, distancefn=L2distanceV)
        Returns distance (scalar), position (2d)

    voronoinoise3d(P, distancefn=L2distanceV)
        Returns distance (scalar), position (3d)
