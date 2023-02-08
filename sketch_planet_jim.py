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
    num_layers = vsketch.Param(3, min_value=2)
    draw_stroke = vsketch.Param(False)
    num_steps = vsketch.Param(1000)
    edge_buffer = vsketch.Param(1, unit="px")
    min_radius_multiplier = vsketch.Param(0.2, decimals=4)
    max_radius_multiplier = vsketch.Param(0.95, decimals=4)
    precision = vsketch.Param(3)

    min_radius = vsketch.Param(0.1, decimals=4, unit="in")

    max_num_inner_circles = vsketch.Param(20)
    max_inner_circles_ratio = vsketch.Param(0.5, decimals=3)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}", landscape=True, center=False)
        vsk.penWidth(f"{self.pen_width}")

        layers = [1 + i for i in range(self.num_layers)]
        bigCircle = MyShape(Point2D(self.width / 2, self.height / 2),
                            min(self.width, self.height) / 2,
                            random_elem(vsk, layers))
        for i in range(self.num_steps):
            if self.debug:
                print(f"{i}/{self.num_steps}")
            bigCircle.spawn_inner_cirlce(vsk, self, layers)
        bigCircle.draw(vsk, self)

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
            shape.circle(inner.center.x,
                         inner.center.y,
                         radius=inner.radius,
                         op="difference")
        return shape

    def draw(self, vsk: vsketch.Vsketch, config):
        if config.draw_stroke:
            vsk.stroke(self.layer)
        else:
            vsk.noStroke()
        vsk.fill(self.layer)
        vsk.shape(self.to_shape(vsk))
        for shape in self.inner_shapes:
            shape.draw(vsk, config)

    def spawn_inner_cirlce(self, vsk, config, layers):
        x = vsk.random(0, 1)
        y = vsk.random(0, 1)
        a = min(x, y)
        b = max(x, y)
        offset = b * self.radius - config.edge_buffer
        theta = 2 * np.pi * a / b
        p = Point2D(a=theta, r=offset) + self.center
        r = maxRadiusAtP(
            self.inner_shapes, p,
            min(self.radius * config.max_inner_circles_ratio,
                self.radius - offset))

        if r is None:
            return None

        r *= np.round(
            vsk.random(config.min_radius_multiplier,
                       config.max_radius_multiplier), config.precision)

        if r < config.min_radius:
            return None
        other_layers = [l for l in layers if l != self.layer]
        layer = random_elem(
            vsk, other_layers) if len(other_layers) >= 1 else self.layer
        newShape = MyShape(p, r, layer)
        self.inner_shapes.append(newShape)
        for _ in range(config.max_num_inner_circles):
            newShape.spawn_inner_cirlce(vsk, config, layers)
