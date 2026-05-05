#mini project
#Student Performance Dashboard

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    "Name": ["A","B","C","D","E"],
    "Marks": [80,90,70,60,85],
    "Dept": ["IT","IT","HR","HR","IT"]
}

df = pd.DataFrame(data)

# Scatter
#sns.scatterplot(x="Name", y="Marks", data=df)
#plt.show()

# Bar
#sns.barplot(x="Dept", y="Marks", data=df)
#plt.show()

# Box
#sns.boxplot(x="Dept", y="Marks", data=df)
#plt.show()

# Heatmap
#sns.heatmap(df.corr(), annot=True)
#plt.show()

# Explanation:
# Scatter → performance
# Bar → dept avg
# Box → outliers
# Heatmap → relation

# Seaborn = statistical visualization
# Matplotlib base use karta hai
# ML me feature analysis
# Heatmap & Boxplot important

# Intro
# Dataset
# Scatter
# Bar
# Histogram
# Box
# Heatmap
# Project

# tips dataset pe:
#
# scatter
# bar
# heatmap

#Graph samajh gaya… toh data samajh gaya

#task
#Restaurant Data Analysis Dashboard
#STEP 0: Dataset Load

'''import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")

print(df.head())'''

#BASIC EDA
# Total rows & columns find karo
# .info() check karo
# .describe() use karo
# Missing values check karo

#RELATION ANALYSIS
#Kya total_bill aur tip ka relation hai?

# sns.scatterplot(x="total_bill", y="tip", data=df)
# plt.show()

#Relation positive hai ya nahi explain karo
#Kya gender ka effect hai?


#DISTRIBUTION ANALYSIS
#sns.histplot(df["total_bill"], bins=20)
#plt.show()

#Most customers kitna bill pay karte hai?

#CATEGORY ANALYSIS
# Kaunsa din sabse zyada earning deta hai?
#Lunch vs Dinner difference?

#OUTLIER DETECTION
#Kya koi extreme bill hai?

#CORRELATION
#Kaunsa feature important hai tip ke liye?

#BONUS
#Full data relation dekho

#FINAL OUTPUT
# Best earning day
# Tip kis pe depend karta hai
# Dinner vs Lunch difference
# Outliers hai ya nahi
# Customer behaviour summary

#REAL INDUSTRY VALUE
# Data Analyst job ka real kaam
# ML se pehle ka most important step








