'''try:
    a = 10
    b = 2
    print(a/b)
except:
   print("can't divide by zero")'''

'''try:
    data = open("data12.txt","r")
    if data:
        print("file open done")
        data.close()
except:
   print("file open error")'''

'''try:
    a = 10
    b = 0
    print(a/b)
except Exception as e:
    print("can't divide by zero")
    print(e)'''

'''try:
    a = 10
    b = 0
    print(a/b)
except ZeroDivisionError:
   print("can't divide by zero")'''

'''try:
    a = 10
    b = 0
    print(a/b)
except (ZeroDivisionError,TypeError):
    print("can't divide by zero")
else:
    print("rest of the code")'''

'''try:
    a = 10
    b = 0
    print(a/b)
except ZeroDivisionError:
    print("can't divide by zero")
else:
    print("rest of the code")
finally:
    print("finally always working")'''

'''try:
    a = 10
    b = 2
    print(a/b)
except ZeroDivisionError:
    print("can't divide by zero")
else:
    print("rest of the code")
finally:
    print("finally always working")'''

'''try:
    age = int(input("enter your age:"))
    if age <=18:
        raise ValueError
    else:
        print("you are old enough to vote!")
except ValueError:
    print("try after 18 years!")'''

'''try:
    age = int(input("enter your age:"))
    if age <= 18:
        raise ValueError
    else:
        print("you are old enough to vote!")
except ZeroDivisionError:
    print("try after 18 years!")'''
