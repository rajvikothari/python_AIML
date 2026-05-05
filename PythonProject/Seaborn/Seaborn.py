#seaborn = advanced version for matplotlib

#Better design (Automatic styling)
#Statistical graph (for using ML)
#Direct work with Pandas DataFrame

#real life example
#Tumhare pass data hai:

# Ex: Students marks, salary data, sales

#Seaborn use

# Relation, Distribution, Pattern

# Why use Seaborn?
# Clean & beautiful graphs
# ML feature analysis
# Correlation check
# Outliers detect

#import seaborn as sns
#import matplotlib.pyplot as plt

#df=sns.load_dataset("tips")
#print(df.head())

#print(df.dtypes)

#sns.scatterplot(x="total_bill", y="tip", data=df)
#plt.show()

#sns.scatterplot(x="total_bill", y="tip", hue="sex", data=df)
#plt.show()

#sns.lineplot(x="total_bill", y="tip", data=df)
#plt.show()

#sns.barplot(x="total_bill", y="tip", data=df)
#plt.show()

#sns.histplot(df['total_bill'], bins=10)
#plt.show()

#sns.boxplot(x="day", y="total_bill", data=df)
#plt.show()

#sns.heatmap(df.corr(), annot=True)
#sns.heatmap(df.corr(numeric_only=True), annot=True)
#plt.show()

#sns.pairplot(df)
#plt.show()

#sns.countplot(x="day", data=df)
#plt.show()

#Real ML use case

#problem customer spending analysis

import seaborn as sns
import matplotlib.pyplot as plt

'''df = sns.load_dataset("tips")
print(df.dtypes)

#step 1 : Relation
sns.scatterplot(x="total_bill", y="tip", data=df)

#step 2 : Distribution
sns.histplot(df["total_bill"])

#step 3 : Correlation
sns.heatmap(df.corr(numeric_only=True),annot=True)
plt.show()'''


