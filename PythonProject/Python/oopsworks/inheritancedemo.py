# Inheritance 3 types: Single type, Multilevel, Multiple
#Single Type
# class Father():#parent,super,base
#     def fData(self):
#         print("father is calling")
#
# class Son(Father):#child,sub,drived
#     def fSon(self):
#         print("son is calling")
#
# son=Son()
# son.fSon()
# son.fData()

#Multilevel
# class GrandFather():
#     def gData(self):
#         print("GrandFather is calling")
# class Father(GrandFather):
#     def fData(self):
#         print("father is calling")
#
# class Son(Father):
#     def fSon(self):
#         print("son is calling")
#
# son=Son()
# son.gData()
# son.fSon()
# son.fData()

#Multiple
class A():
    def gData(self):
        print("A is calling")
class B():
    def bData(self):
        print("B is calling")

class C(A,B):
    def fCon(self):
        print("C is calling")

c=C()
c.bData()
c.gData()
c.fCon()
