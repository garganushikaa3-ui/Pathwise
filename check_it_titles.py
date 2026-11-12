import pandas as pd

df = pd.read_excel('data/Essential Skills.xlsx', sheet_name='Essential Skills')
soc_col = df.columns[0]
title_col = df.columns[1]

# Find all 15-xxxx
it_rows = df[df[soc_col].str.startswith('15-', na=False)][[soc_col, title_col]].drop_duplicates()
print("Unique titles in 15-xxxx:")
for title in sorted(it_rows[title_col].unique()):
    print("-", title)
