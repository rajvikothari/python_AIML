# Classes
# Objects
# Encapsulation
# Inheritance
# Abstraction
# Polymorphism

'''Abstraction is the concept of hiding complex implementation
details and showing only the essential features of an object
or function.'''


# you use the ABC (Abstract Base Class) from the abc module.
from abc import ABC, abstractmethod

# abstract class
class Shape(ABC):
    def area(self):
        pass

    def perimeter(self):
        pass


# sub class

class Ractangle(Shape):
    def __init__(self, width, height):
        self.width=width
        self.height=height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2*(self.width + self.height)


class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def perimeter(self):
        return  2 * 3.14 * self.radius



ract=Ractangle(5,4)
print("area: ", ract.area())
print("perimeter: ", ract.perimeter())


cir=Circle(7)
print("area: ", cir.area())
print("perimeter: ", cir.perimeter())

