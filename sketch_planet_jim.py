import vsketch
from point2d import Point2D
import numpy as np


def random_elem(vsk: vsketch.Vsketch, items):
    return items[int(vsk.random(0, 1) * len(items))]


class PlanetJimSketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    pen_width = vsketch.Param(0.7, decimals=3, unit="mm")
    num_layers = vsketch.Param(1)
    num_steps = vsketch.Param(1000)
    edge_buffer = vsketch.Param(1, unit="px")

    # maxRadiusRatio = vsketch.Param(0.2, decimals=5)
    min_radius = vsketch.Param(0.1, decimals=4, unit="in")

    max_inner_circles_ratio = vsketch.Param(2.0, decimals=3)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}", landscape=True, center=False)
        vsk.penWidth(f"{self.pen_width}")

        layers = [1 + i for i in range(self.num_layers)]
        bigCircle = MyShape(Point2D(self.width / 2, self.height / 2),
                            min(self.width, self.height) / 2,
                            random_elem(vsk, layers))
        for i in range(self.num_steps):
            bigCircle.spawn_inner_cirlce(vsk, self.edge_buffer,
                                         self.min_radius, layers,
                                         self.max_inner_circles_ratio)
        bigCircle.draw(vsk)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlanetJimSketch.display()


def maxRadiusAtP(shapes, p, upperBound):
    m = upperBound
    for s in shapes:
        dist = (p - s.center).r
        if dist < s.radius:
            return None
        m = min(dist - s.radius, m)
    return m


class MyShape:

    def __init__(self, center, r, layer):
        self.center = center
        self.radius = r
        self.layer = layer
        self.inner_shapes = []

    def to_shape(self, vsk: vsketch.Vsketch):
        shape = vsk.createShape()
        shape.circle(self.center.x, self.center.y, radius=self.radius)
        for inner in self.inner_shapes:
            shape.circle(inner.center.x + self.center.x,
                         inner.center.y + self.center.y,
                         radius=inner.radius,
                         op="difference")
        return shape

    def draw(self, vsk: vsketch.Vsketch):
        vsk.fill(self.layer)
        vsk.shape(self.to_shape(vsk))
        for shape in self.inner_shapes:
            shape.draw(vsk)

    def spawn_inner_cirlce(self, vsk, edge_buffer, min_radius, layers,
                           max_inner_circles_ratio):
        theta = vsk.random(0, np.pi * 2)
        max_r = self.radius - edge_buffer
        offset = vsk.random(0, max_r)
        p = Point2D(a=theta, r=offset)
        r = maxRadiusAtP(self.inner_shapes, p, max_r)
        if r is None or r < min_radius:
            return None

        other_layers = [l for l in layers
                        if l != self.layer] if len(layers) > 1 else layers
        layer = random_elem(vsk, other_layers)
        newShape = MyShape(p, r, layer)
        maxInnerCircles = int(r * max_inner_circles_ratio)
        for _ in range(maxInnerCircles):
            newShape.spawn_inner_cirlce(vsk, edge_buffer, min_radius, layers,
                                        max_inner_circles_ratio)

        self.inner_shapes.append(newShape)
