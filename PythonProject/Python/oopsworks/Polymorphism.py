# Polymorphism means "many forms".
# It allows objects of different classes to be treated through a common interface.

# Type	                Meaning	                Python Support
# Compile-time (Static)	Method Overloading	    Not supported natively
# Runtime (Dynamic)	    Method Overriding	    Supported via inheritance



# Method Overriding
# class Company:
#     def showData(self, name):
#         print("hello!", name)
#
# class Employee(Company):
#     def showData(self):
#         print("hello from method 2")
#
# emp=Employee()
# emp.showData()


'''Polymorphism with Inheritance'''

# class Animal:
#     def speak(self):
#         return "Some sound"
#
# class Dog(Animal):
#     def speak(self):
#         return "Woof!"

# class Cat(Animal):
#     def speak(self):
#         return "Meow!"
#
# animals=[Dog(), Cat(), Animal()]
# for animal in animals:
#     print(animal.speak())


'''Polymorphism with Functions and Objects'''

# class Dog:
#     def speak(self):
#         return "Woof!"
#
# class Cat:
#     def speak(self):
#         return "Meow!"
#
# def animal_sound(animal):
#     print(animal.speak())
#
# dog=Dog()
# cat=Cat()
#
# animal_sound(dog)
# animal_sound(cat)


'''super keyword'''

# class Animal:
#     def speak(self):
#         print("animal")
#
# class Dog(Animal):
#     def speak(self):
#         super().speak()
#         print('dog')
#
# dog=Dog()
# dog.speak()


# task: to do same with super keyword
class Bank():
    def getROI(self):
        return 10

class Sbi(Bank):
    def getROI(self):
        return 8

sbi=Sbi()
print(sbi.getROI())
