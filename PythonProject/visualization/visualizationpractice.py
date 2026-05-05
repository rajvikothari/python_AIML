'''What is visualization
Line plot
Bar chart
Histogram
Scatter
Customization
Mini project'''
from seaborn import barplot

#Converting the data into a graph
#Line plot

'''import matplotlib.pyplot as plt

x = [1,2,3,4,5,6]
y = [10,15,20,30,40,50]

plt.title('Line chart')
plt.plot(x,y, marker='o', color='red')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.show()'''

#Bar chart

'''import matplotlib.pyplot as plt

names = ['Aesha','Rajvi','Dhruv','Dhruvil']
marks = ['60','70','80','90']


plt.bar(names, marks, color='blue')
plt.title('student marks')

plt.xlabel("Students")
plt.ylabel("marks")

plt.show()'''

#Histogram

'''import matplotlib.pyplot as plt
data = [10,20,20,30,30,40,40,40,50,55]
plt.hist(data, color='red')
plt.title('Histogram')

plt.show()'''

#Scatter

'''import matplotlib.pyplot as plt

x = [1,2,3,4]
y = [10,20,40,30]

plt.scatter(x,y, color="red")
plt.title('scatter plot')

plt.show()'''

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

''' TASK 1: Basic Understanding

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
Average marks '''

#import pandas as pd
#import matplotlib.pyplot as plt

'''data = {
    "Name": ["A","B","C","D","E"],
    "Marks": [80, 90, 70, 60, 85],
    "Dept": ["IT","IT","HR","HR","IT"]
}

df = pd.DataFrame(data)'''

# 1. Data print
#print("All Data:")
#print(df)

# 2. .head() use karo
#print("First rows")
#print(df.head())

# 3. .info() check karo
#print("Data information")
#print(df.info())

#4. Average marks
#marks = df["Marks"].mean()
#print("Average marks:", marks)


'''TASK 2: Matplotlib Basic
Line graph banao (Marks vs Index)
Bar chart banao (Name vs Marks)
Graph me:
Title add karo
X label
Y label with Customization'''

#Line graph banao (Marks vs Index)
'''import matplotlib.pyplot as plt

index = [1, 2, 3, 4, 5]
marks = [60, 70, 80, 90, 65]

plt.plot(index, marks, color='red', marker='o')

plt.title("Exam Results")
plt.xlabel("Index")
plt.ylabel("Marks")

plt.show()'''

# 2 Bar chart banao (Name vs Marks)

'''import matplotlib.pyplot as plt

names = ['Aesha','Rajvi','Dhruv','Dhruvil']
marks = ['65','75','70','85']

plt.bar(names, marks, color='blue')

plt.title('Student Result')
plt.xlabel("Students")
plt.ylabel("marks")

plt.show()'''


#Data Analysis

#Dept-wise average marks nikaalo
#Topper find karo
#Pass/Fail column add karo
#condition: Marks >= 75 → Pass
#Kitne Pass aur Fail hain count karo


#Dept-wise average marks nikaalo
#depth_avg = df.groupby("Dept")["Marks"].mean()
#print("Dept-wise Average", depth_avg)

#Topper find karo
#topper = df.loc[df["Marks"].idxmax()]
#print("Topper", topper)

#Pass/Fail column add karo
#condition: Marks >= 75 → Pass
#df["Result"] = df["Marks"].apply(lambda x: "Pass" if x >= 75 else "Fail")
#print("Updated Data:", df)

#How many students are pass or fail
#count = df["Result"].value_counts()
#print("Pass/Fail Count:", count)


#Visualization Advanced
#Box plot (Dept vs Marks)
#Histogram (Marks distribution)
#Heatmap (correlation)

#Box plot (Dept vs Marks)

import seaborn as sns

# = pd.DataFrame(data)

#sns.boxplot(x="Dept", y="Marks", data=df)
#plt.title('Box plot: Dept vs Marks')
#plt.show()


#Histogram (Marks distribution)
#sns.histplot(df['Marks'], bins=5)
#plt.title("Histogram of marks")
#plt.xlabel("Marks")
#plt.ylabel("Frequency")
#plt.show()

#Heatmap (correlation)
#sns.heatmap(df.corr(numeric_only=True),annot=True)
#plt.title("Correlation Heatmap")
#plt.show()

'''Real Dataset
import seaborn as sns

df = sns.load_dataset("tips")

.head() aur .info() dekho
Scatter plot (total_bill vs tip)
Histogram (total_bill)
Box plot (day vs total_bill)
Heatmap (correlation)'''


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


#import seaborn as sns
#import matplotlib.pyplot as plt


# Load dataset
#df = sns.load_dataset("tips")

# 1. .head() and .info()

'''print(df.head())
print("Dataset Info:")
print(df.info())'''


# 2. Scatter Plot (total_bill vs tip)
'''sns.scatterplot(x="total_bill", y="tip", hue="sex", data=df)
plt.title("Total Bill vs Tip")
plt.show()'''


# 3. Histogram (total_bill)
'''sns.histplot(df["total_bill"], bins=10)
plt.title("Distribution of Total Bill")
plt.xlabel("Total Bill")
plt.ylabel("Frequency")
plt.show()'''


# 4. Box Plot (day vs total_bill)
'''sns.boxplot(x="day", y="total_bill", data=df)
plt.title("Day vs Total Bill")
plt.show()'''


# 5. Heatmap (correlation)
'''sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()'''

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''Mini Project
Student Performance Dashboard
student ko karna hai:
Dataset create karo (kam se kam 6 students)
Columns:
Name
Marks
Dept'''

#import pandas as pd
'''data = {
    "Name": ["Aesha", "Rajvi", "Dhruv", "Dhruvil", "isha", "Aarvi"],
    "Marks": [85, 72, 90, 65, 78, 88],
    "Dept": ["IT", "CS", "IT", "HR", "CS", "IT"]
}'''

#df = pd.DataFrame(data)

#print(df)

'''Analysis:
Average marks
Topper
Dept-wise avg

#Average marks
avg_marks = df["Marks"].mean()
print("Average marks", avg_marks)

#Topper
topper = df.loc[df["Marks"].idxmax()]
print("topper",topper)

#Dept-wise avg
dept_avg = df.groupby("Dept")["Marks"].mean()
print("Depth wise average",dept_avg)'''


'''Visualization:
Bar chart
Scatter plot
Box plot
Heatmap'''

#Bar chart

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    "Name": ["Aesha", "Rajvi", "Dhruv", "Dhruvil", "isha", "Aarvi"],
    "Marks": [85, 72, 90, 65, 78, 88],
    "Dept": ["IT", "CS", "IT", "HR", "CS", "IT"]
}

df = pd.DataFrame(data)

print(df)

'''depth_avg = df.groupby("Dept")["Marks"].mean().reset_index()
sns.barplot(x="Dept", y="Marks", data=depth_avg)
plt.title("Depth-wise Average Marks")
plt.show()'''


#Scatter plot

'''sns.scatterplot(x=df.index, y="Marks", data=df)
plt.title("Marks Distribution")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.show()'''


#Box plot

'''sns.boxplot(x="Dept", y="Marks", data=df)
plt.title("Dept vs Marks")
plt.show()'''


#Heatmap

'''sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Heatmap")
plt.show()'''
