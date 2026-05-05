# datatype : Type of value is known as its datatype.
# types : Number, Sequences, Boolean, Dictionary and Set
# sub-datatypes : Number => int, float and complex, Sequences => string, list and tuple
# immutable and mutable : list, dictionary and set are mutable rests are immutable.

# Number
# int : non-decimal value
#num = 10
#print(num)
#print(type(num))
#print(isinstance(num, int))


# float : decimal value
# num = 10.25
# print(num)
# print(type(num))
# print(isinstance(num, int))


# complex : It is the combination of real and imaginary number.
# num = 2j + 1
# print(num)
# print(type(num))
# print(isinstance(num, complex))


# Sequences
# string : sequences of characters
# name = 'rajvi'
# username = "admin"
# print(name, username)
# print(type(name), type(username))
# name = 'waytocode'
# print(name[3])      # extract single value
# print(name[2:6])    # slicing => extract sequences of character
# print(name[2:])
# print(name[:6])


# list : collection of data stored under single variable which is wrapped/enclosed in [] with comma separation whose index starts from 0.
# data = [1, 2, 3, 4, 5, 6]
# print(data)
# # print(type(data))
# # print(data[2])
# # print(data[1:4])
# data.append(7)
# data.append(8)
# data.append(9)
# print(data)
# data.pop()
# data.pop(3)
# print(data)


# tuple : collection of data stored under single variable which is wrapped/enclosed in () with comma separation whose index starts from 0.
# tuple is immutable
# data = (1, 2, 3, 4, 5, 6)
# print(data)
# print(type(data))
# print(data[2])
# print(data[1:4])


# boolean
# condition1 = True
# condition2 = False
# print(condition1, condition2)
# print(type(condition1), type(condition2))
# print(bool(0))
# print(bool(1))
# print(bool(-100))
# print(bool('rajvi'))


# dictionary : keyed collection of data wrapped in {} with comma separation.
# data = {
#     'username': 'rajvi',
#     'password': 123456
# }
#
# print(data)
# print(type(data))
# print(data['username'])
# print(data['password'])
# print(data.keys())
# print(data.values())
# data['isAdmin'] = True
# print(data)

# TASK : Remove key value from dictionary
#data = {
#     'firstname' : 'rajvi',
#     'lastname' : 'Kothari'
# }
#print(data)
#print(type(data))
#print(data['firstname'])
#print(data['lastname'])
#print(data.keys())
#print(data.values())
#print(data)
#data.pop()

# set : unique collection of data wrapped in {} with comma separation which jumble when it is invoked.
# data = {'html', 'css', 'js', 'python', 'js', 'java', 'html'}
# print(data)
# print(type(data))

# TASK : Add and Remove data from set practice rajvi
#data = {"hello", "how", "are", "you", "how's", "you", "how's"}
#print(data)
#print(type(data))


