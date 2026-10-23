import pandas as pd


df = pd.read_excel("main.xlsx", nrows=10, dtype=str)

data = []

for v in df.to_dict(orient='records'):
    data.append(dict(v))

print(data)
