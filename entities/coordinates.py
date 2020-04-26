import math

class Vector:
    threshold = 1e-16

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __eq__(self, other):
        return self == other or (self - other).length() < Vector.threshold

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def round(self) -> (int, int):
        return int(self.x), int(self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return (a for a in (self.x, self.y))

    @staticmethod
    def dist(v1, v2):
        return (v2 - v1).length()

if False:
    c = Vector(2,3)
    d = Vector(17, 18)
    print(c + d)
    print(d - c)
    print(c * d)
    print(c * 3)
    print(d * .7)
    a,b = d
    print(a, b)