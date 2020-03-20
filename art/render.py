from . import png
import multiprocessing


class KS:
    def __init__(self, Pi, Pj):
        self.x = (130704498139423.0 ** 0.5)/17453848.0
        self.y = (376969570242446.0 ** 0.5)/22680362.0
        self.sx = (Pj * self.x) % 1.0
        self.sy = (Pi * self.y) % 1.0

    def getsample(self):
        self.sx = (self.sx + self.x) % 1.0
        self.sy = (self.sy + self.y) % 1.0
        return (self.sx, self.sy)


def render_row(y, width, shader, samples):
    # shader, samples attached as a closure
    row = []
    for x in range(width):
       sampler = KS(x,y)
       C = []
       for s in range(samples):
           sample = sampler.getsample()
           C.append(shader((sample[0] + x)/width, (sample[1] + y)/width))

       row.append(sum(c[0] for c in C) / samples)
       row.append(sum(c[1] for c in C) / samples)
       row.append(sum(c[2] for c in C) / samples)

    return [int(255.0 * (min(1.0,max(0.0,c)) ** (1.0/2.2))) for c in row]


def render(shader, filename, width=1280, height=720, samples=16):
    with multiprocessing.Pool() as pool:
        image = pool.starmap(render_row, zip(range(height),[width]*height, [shader]*height,[samples]*height), 16)

    # alternative implementation for single process operation:
    # image = [render_row(*x) for x in zip(range(height),[width]*height, [shader]*height,[samples]*height)]

    writer = png.Writer(width=width, height=height, compression=9)
    with open(filename, 'wb') as fp:
        writer.write(fp, image)

    return
