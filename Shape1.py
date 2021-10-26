import math
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point({0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return "{0.x!r},{0.y!r}".format(self)

class Circle(Point):
    def __init__(self, radius,x=0, y=0):
        super().__init__(x,y)
        self.radius=radius

    def area(self):
        return math.pi*(self.radius**2)

    def __repr__(self):
        return "Circle({0.radius!r},{0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return "{0.x!r},{0.y!r}".format(self)

