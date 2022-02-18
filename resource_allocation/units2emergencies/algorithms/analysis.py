import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('progress.csv')
print(df.columns)
df.drop(columns=['Unnamed: 0'], inplace=True)
df.plot(legend=False)
plt.show()