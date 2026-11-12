import pandas as pd

df = pd.read_excel('data/Essential Skills.xlsx', sheet_name='Essential Skills')
print('Total rows:', len(df))
soc_code_col = df.columns[0]
title_col = df.columns[1]
print('Unique occupations total:', df[title_col].nunique())

it_df = df[df[soc_code_col].str.startswith('15-', na=False)]
unique_it = it_df[[soc_code_col, title_col]].drop_duplicates()
print(f'Computer and Mathematical Occupations (15-xxxx): {len(unique_it)}')
for idx, row in unique_it.iterrows():
    print(f"{row[soc_code_col]} | {row[title_col]}")

print("\nSample skills for Software Developers:")
sd_df = df[df[title_col].str.contains('Software Developer', case=False, na=False)]
print(sd_df[sd_df['Scale ID'] == 'IM'][['Element Name', 'Data Value']].sort_values(by='Data Value', ascending=False).head(10))
