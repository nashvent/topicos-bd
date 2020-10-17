import pandas as pd
df=pd.read_csv('data/stories.csv', sep=',',header=None)

for i in range(1):
    print(df[1][i])