import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='final carrer sheet')
df = df.dropna(subset=['Carrer name'])
print(f"Total valid careers: {len(df)}")

df_occ = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='Occupation Data')
occ_map = dict(zip(df_occ['O*NET-SOC Code'], df_occ['Description']))

for idx, row in df.iterrows():
    soc = row['O*NET-SOC Code']
    name = row['Carrer name']
    desc = occ_map.get(soc, "Description not found in Occupation Data")
    print(f"[{soc}] {name} | Edu: {row['Education/Qualification']} | Salary: {row['Median salary']} | Outlook: {row['Job outlook']}")
