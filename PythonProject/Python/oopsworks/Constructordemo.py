# A constructor is a special type of method (function) which is used to initialize
# the instance members of the class.

# Parameterized Constructor
# Non-parameterized Constructor


# Parameterized Constructor
# class Employee:
#     def __init__(self,id,name):
#         self.uId=id
#         self.uName=name
#         print("constructor is calling")
#
#     def showData(self):
#         print(self.uId,self.uName)
#
# emp=Employee(101,"aashu")
# emp2=Employee(102,"jack")
#
# emp.showData()
# emp2.showData()


# Non-parameterized Constructor
# class Employee:
#     def __init__(self):
#         print("constructor is calling")
#
# emp=Employee()
# emp2=Employee()

#Multiple
class Employee:
    def __init__(self):
        print("first constructor is calling")
    def __init__(self):
        print("second constructor is calling")

emp=Employee()
