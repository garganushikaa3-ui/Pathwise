import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df_skills = pd.read_excel('data/Essential Skills.xlsx', sheet_name='Essential Skills')
soc_col = df_skills.columns[0]
title_col = df_skills.columns[1]

df_final = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='final carrer sheet').dropna(subset=['Carrer name'])

print("Unique titles in Essential Skills:")
all_titles = set(df_skills[title_col].dropna().unique())

matched_titles = 0
for idx, row in df_final.iterrows():
    name = row['Carrer name']
    soc = row['O*NET-SOC Code']
    if name in all_titles:
        matched_titles += 1
    else:
        # find closest match
        matches = [t for t in all_titles if name.lower() in t.lower() or t.lower() in name.lower()]
        print(f"Direct miss: '{name}' ({soc}) -> closest: {matches[:3]}")

print(f"\nTitle exact matches: {matched_titles} / {len(df_final)}")
