#EDA
#EDA = Exploratory Data Analysis


#Why EDA
#For Data Understanding
#For pattern find
#Outliers detect
#for ML model improve

#Visualization
#Converting the data into a graph


#Tools
#Matplotlib
#Seaborn

#MAtplotlib
#Matplotlib = for creating python graph tool
#Captures data visually (graphs)
#Numbers -> Graph

#MArks List:
#[80, 90, 70, 60]

#Why

#Data analysis(EDA)
#ML me pattern dekhne
#Reports / dashboard
#Business Decisions

#Core Concepts
#Graph =
# X-axis(Horizontal)
# Y-axis(Vertical)

'''#Line Plot(Most Basic)
import matplotlib.pyplot as plt
#
#Step
x=[1,2,3,4]
y=[10,20,30,40]

plt.plot(x,y)
plt.title('line plot')

plt.xlabel('x')
plt.ylabel('y')

plt.show()'''

#Bar Chart(Comparison)
'''import matplotlib.pyplot as plt
names = ["A","B","C"]
marks = [80,90,65]

plt.bar(names,marks)
plt.title("Student marks")

plt.xlabel("Students")
plt.ylabel("marks")

plt .show()'''

#Histogram(Distribution)
'''import matplotlib.pyplot as plt
data = [10.20,20,20,30,40,40,40,50]
plt.hist(data)
plt.title("Data Distribution")
plt.show()'''

#Scatter Plot(Relation)
import matplotlib.pyplot as plt

#x = [1,2,3,4]
#y = [10,15,25,30]
#plt.scatter(x,y)
#plt.title("Scatter Plot")

#plt.show()

#Customization
#import matplotlib.pyplot as plt

#x = [1,2,3]
#y = [10,20,30]

#plt.plot(x,y,color="red",marker="o",linestyle="-")
#plt.show()

#Multiple Graphs
#import matplotlib.pyplot as plt
#x = [1,2,3]

#y1 = [10,20,30]
#y2 = [15,25,35]

#plt.plot(x,y1,label="line 1",color="blue",marker="o")
#plt.plot(x,y2,label="line 2",color="red",marker="o")

#plt.legend()
#plt.show()

#Subplots
import matplotlib.pyplot as plt

#x = [1,2,3]
#y = [10,20,30]
#plt.subplot(1,2,1)
#plt.plot(x,y, color="blue", marker="o")

#plt.subplot(1,2,2)
#plt.bar(x,y, color="red")

#plt.show()

#REAL DATA
#import pandas as pd
#import matplotlib.pyplot as plt

#data = {
#    "name":["A","B","C","D"],
#    "marks":[70,90,80,40]
#}
#df=pd.DataFrame(data)

#plot section

#plt.bar(df["name"],df["marks"])
#plt.title("Student Performance")

#plt.show()

#import matplotlib.pyplot as plt

#months = ["Jan","Feb","Mar","Apr"]
#sales = [100,200,150,300]

#plt.plot(months, sales, marker='o')

#plt.title("Monthly Sales")
#plt.xlabel("Months")
#plt.ylabel("Sales")
#plt.show()


#Important Functions
# | Function  | Use          |
# | --------- | ------------ |
# | plot()    | line graph   |
# | bar()     | comparison   |
# | hist()    | distribution |
# | scatter() | relation     |
# | title()   | heading      |
# | xlabel()  | x name       |
# | ylabel()  | y name       |
# | legend()  | label show   |
# | show()    | display      |


'''Matplotlib = plotting library
Used in EDA
Basic graphs banane ke liye
Seaborn = advanced version'''

'''What is visualization
Line plot
Bar chart
Histogram
Scatter
Customization
Mini project'''

'''task
Create:

line graph
bar chart
histogram

'''

'''
TASK 1: Basic Understanding

import pandas as pd

data = {
    "Name": ["A","B","C","D","E"],
    "Marks": [80, 90, 70, 60, 85],
    "Dept": ["IT","IT","HR","HR","IT"]
}

df = pd.DataFrame(data)

Data print karo
.head() use karo
.info() check karo
Average marks nikaalo



TASK 2: Matplotlib Basic
Line graph banao (Marks vs Index)
Bar chart banao (Name vs Marks)
Graph me:
Title add karo
X label
Y label


#Data Analysis

Dept-wise average marks nikaalo
Topper find karo
Pass/Fail column add karo
condition: Marks >= 75 → Pass
Kitne Pass aur Fail hain count karo


#Visualization Advanced
Box plot (Dept vs Marks)
Histogram (Marks distribution)
Heatmap (correlation)


#Real Dataset
import seaborn as sns

df = sns.load_dataset("tips")

.head() aur .info() dekho
Scatter plot (total_bill vs tip)
Histogram (total_bill)
Box plot (day vs total_bill)
Heatmap (correlation)

Mini Project
Student Performance Dashboard
student ko karna hai:
Dataset create karo (kam se kam 6 students)
Columns:
Name
Marks
Dept


Analysis:
Average marks
Topper
Dept-wise avg

Visualization:
Bar chart
Scatter plot
Box plot
Heatmap
#ek clean dashboard (graphs + results)

'''