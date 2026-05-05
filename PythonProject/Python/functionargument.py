#fun with parm

'''def add(a,b):
    print(a+b)

x=10
y=20
x=int(input("Enter the X:"))
y=int(input("Enter the Y:"))
add(x,y)'''

#fun with return

'''def add():
    a=10
    b=20
    c=a+b
    return c
print("total add data",add())'''


#types of arguments
#required, Keyword, default, Variable-length

#required
'''def showdata(name,city="Ahmedabad"):
    print("hello",name)

showdata("rajvi")'''

#Keyword
'''def showInfo(name,number,city):
    print("hello",name,number,city)
showInfo(name="Rajvi",number="9909634567",city="Ahmedabad")'''

#Variable-length
'''def showNames(*names):
    print(names)
    for i in names:
        print(i)
showNames("rajvi","kothari","aarvi","shah")'''

