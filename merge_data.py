import pandas as pd
import numpy as np

svy18 = pd.read_csv('Survey_2018.csv')
svy19 = pd.read_csv('Survey_2019.csv')
svy20 = pd.read_csv('Survey_2020.csv')

for y, d in zip(range(18, 20+1), [svy18, svy19, svy20]):
	print(f'Survey 20{y} Columns:', d.columns)

print('Make sure that one column you want to merge is across in 3 dataset.')
col_merge = input('Which one column that you want to merge: ')
data = {f'20{y}': d[col_merge] for y, d in zip(range(18, 20+1), [svy18, svy19, svy20])}

df = pd.DataFrame(data)
df.to_csv(f'All {col_merge} Survey.csv', index=False)
