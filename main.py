from math import hypot, atan2, sin, cos, pi, radians
import cairo
import colorsys
import random

class Model(object):
    def __init__(self):
        self.particles = []
    def add(self, x, y, m=1.0):
        self.particles.append((x, y, m))
    def test(self, x, y):
        dx = 0
        dy = 0
        for px, py, pm in self.particles:
            d = hypot(x - px, y - py)
            angle = atan2(y - py, x - px)
            dx += pm * cos(angle) / d
            dy += pm * sin(angle) / d
        angle = atan2(dy, dx) + pi / 2
        dx = cos(angle)
        dy = sin(angle)
        return (dx, dy)

def points(sides):
    x = 0.5
    y = 0.5
    rotation = 0
    angle = 2 * pi / sides
    rotation = rotation - pi / 2
    angles = [angle * i + rotation for i in range(sides)]
    d = 0.35
    return [(x + cos(a) * d, y + sin(a) * d) for a in angles]

def draw_path(dc, model, scale, width, r, g, b):
    n = 128
    f = 1 / 1024.0
    sx = random.random()
    sy = random.random()
    for m in [-1, 1]:
        x, y = sx, sy
        dc.move_to(x, y)
        for j in range(n):
            dx, dy = model.test(x, y)
            dc.line_to(x, y)
            p = 1.0 - (j / (n - 1.0)) ** 2
            a = p * 0.3
            dc.set_source_rgba(r, g, b, a)
            dc.set_line_width(width * p / scale)
            if j:
                dc.stroke()
            dc.move_to(x, y)
            x += dx * f * m
            y += dy * f * m
            if x < -0.1 or y < -0.1 or x > 1.1 or y > 1.1:
                break

def main():
    size = 4096
    scale = size
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size, size)
    dc = cairo.Context(surface)
    dc.set_line_cap(cairo.LINE_CAP_ROUND)
    dc.set_line_join(cairo.LINE_JOIN_ROUND)
    dc.scale(scale, scale)
    dc.set_source_rgb(0, 0, 0)
    dc.paint()
    model = Model()
    for x, y in points(5):
        model.add(x, y)
    model.add(0.5, 0.5, 0.1)
    for i in range(512):
        h = random.random() * 0.06 + 0.04
        s = random.random() * 0.8 + 0.2
        v = random.random() * 0.2 + 0.8
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        w = random.random() * 48 + 16
        draw_path(dc, model, scale, w, r, g, b)
    surface.write_to_png('output.png')

if __name__ == '__main__':
    main()
