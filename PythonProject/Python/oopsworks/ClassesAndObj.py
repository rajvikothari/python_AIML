class Employee:
    id=101
    name="aashu"
    def showData(self):
        print(self.id,self.name)

emp=Employee()
# emp1=Employee()
emp.showData()
# emp1.showData()
# del emp.id
# print(emp.id)

del emp
emp.showData()

