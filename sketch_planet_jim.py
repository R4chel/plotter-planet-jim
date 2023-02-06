import vsketch
from shapely.geometry import Point

def random_elem(vsk: vsketch.Vsketch, items):
    return items[int(vsk.random(0, 1) * len(items))]

class PlanetJimSketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    pen_width = vsketch.Param(0.7, decimals=3, unit="mm")
    num_layers = vsketch.Param(1)
    # maxRadiusRatio = vsketch.Param(0.2, decimals=5)
    # maxInnerCircles = vsketch.Param(10)

    def random_point(self, vsk: vsketch.Vsketch):
        return Point(vsk.random(0, self.width), vsk.random(0, self.height))

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}", landscape=True, center=False)
        vsk.penWidth(f"{self.pen_width}")

        layers = [1 + i for i in range(self.num_layers)]
        bigCircle = MyShape(self.width/2, self.height/2, min(self.width, self.height)/2, random_elem(vsk, layers))
        bigCircle.draw(vsk)


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlanetJimSketch.display()


class MyShape:
    def __init__(self,x,y,r, layer):
        self.x = x
        self.y = y
        self.radius = r
        self.layer = layer 

    def to_shape(self, vsk: vsketch.Vsketch):
        shape = vsk.createShape()
        shape.circle(self.x,self.y,radius=self.radius)
        return shape

    def draw(self, vsk:vsketch.Vsketch):
        vsk.fill(self.layer)
        vsk.shape(self.to_shape(vsk))

