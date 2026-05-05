'''NumPy = Numerical Python

Python list slow hoti hai
NumPy array fast hota hai
Heavy calculations (ML/AI) keliye use hota hai

real example
1 student ka marks = easy
10,000 students ka marks analyze = heavy

python list = slow
NumPy = lightning fast

#Why Numpy?
fast computation(C Language backend)
Less Memory use Mathematical Opertions easy ML, AI, Data Science ka base

#NumPy me sab kuch array hota hai'''

#import numpy as np
#arr=np.array([1,2,3,4,5,6])
#print(arr)

#a = [1,2,3]
#b = [4,5,6]

#print(a + b) #list

#a = np.array([1,2,3])
#b = np.array([4,5,6])

#print(a + b)

'''Types of Array
 1D Array
 2D Array
 3D Array'''

 #1D Array
 #np.array([1,2,3])
 #2D Array
 #np.array([[1,2],[3,4]])
 #3D Array([])
 #np.array([[[1,2],[3,4]]])'''

 #important Methods
 #a=np.zeros((2,3))
 #print(a)
 #ML me initial matrix banane ke liye use hota hai

#.ones()
import numpy as np
#a=np.ones((2,3))
#print(a)
#create array filled with 1s.

#arange()
#a=np.arange(1,10)
#print(a)
#range jaisa but array return karta hai

#inspace()
#a=np.linspace(0,10,5)
#print(a)

#reshape()
#arr = np.array([1,2,3,4,5,6])
#print(arr.reshape(2,3))
#data ko matrix me convert karta hai

#shape
#arr = np.array([[1,2,3],[4,5,6]])
#print(arr.shape)
#rows,columns batata hai

#ndim
#arr = np.array([[1,2,3],[4,5,6]])
#print(arr.ndim)
#dimension batata hai

#dtype
#arr = np.array([1,2,3])
#print(arr.dtype)
#data type batata hai

#indexing & Slicing
#arr = np.array([10,20,30,40])
#print(arr[1])
#print(arr[1:3])

# 2D Indexing
arr = np.array([[1,2,3],
               [4,5,6]])
print(arr[0,2])

#Mathamatical Operations
#arr = np.array([1,2,3,4])
#print(arr+2)
#print(arr*2)

#Aggregation Functions

#arr = np.array([1,2,3,4])
#print(arr.sum())
#print(arr.mean())
#print(arr.min())
#print(arr.max())


#Random Numbers(ML me Important)
#np.random.rand(3)
#np.random.randint(1,10,5)


#important numpy as np

#marks = np.array([50,60,70,80,90])
#print(marks.mean())
#Average nikalna = ML preprocessing

#Numpy faster than list because c Backend
# Used in ML, AI, Data Science
# pandas built on numpy
# supports vectorization


#create array of 10 numbers
# arr = np.array([1,2,3,4,5,6,7,8,9,10])
# print(arr.sum())
# print(arr.mean())
# print(arr.min())
# print(arr.max())
# print(arr.reshape(2,5))

