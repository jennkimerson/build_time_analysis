import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# import data from buildtime_src (v14-16 data)
df = pd.read_excel(r'/Users/jenkim/Desktop/Env/build_time_analysis/buildtime_src (v14-16 data).xlsx')
# data = pd.DataFrame(df, columns=["size", "duration"])
# print(data)


# Select necessary data points
X = df['size'].to_numpy()
y = df['duration'].to_numpy()
# print(X)
# print(y)


# Select random 300 rows with colums size and duration]
# sample = df.sample(n=300)
# print(sample)

# Scatter Plot

# df.plot(x='size', y='duration', kind='scatter')
# plt.show()


# Linear Regression
lin_reg = LinearRegression()
lin_reg.fit(X.reshape(-1, 1), y)

plt.scatter(X, y, color='red')
plt.plot(X, lin_reg.predict(X.reshape(-1, 1)), color='blue')

# Regression
mymodel = np.poly1d(np.polyfit(X, y, 2))
myline = np.linspace(min(X), max(X), len(X))
plt.scatter(X, y)
plt.plot(myline, mymodel(myline))


# Graph
plt.title("Build Time Analysis (Size vs. Duration)")
plt.xlabel('Size')
plt.ylabel('Duration')
plt.show()
