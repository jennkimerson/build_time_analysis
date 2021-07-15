import pandas as pd

df = pd.read_excel(r'YOUR_FILE_PATH/buildtime_src (v14-16 data).xlsx')
# print(df)

sample = df.sample(n=300)
print(sample)
