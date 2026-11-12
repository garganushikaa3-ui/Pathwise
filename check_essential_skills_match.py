import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df_skills = pd.read_excel('data/Essential Skills.xlsx', sheet_name='Essential Skills')
soc_col = df_skills.columns[0]
element_col = df_skills.columns[3]
scale_col = df_skills.columns[4]
val_col = df_skills.columns[6]

df_final = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='final carrer sheet').dropna(subset=['Carrer name'])
soc_list = df_final['O*NET-SOC Code'].astype(str).str.strip().tolist()

found_count = 0
for soc in soc_list:
    subset = df_skills[(df_skills[soc_col].astype(str).str.strip() == soc) & (df_skills[scale_col] == 'IM')]
    if len(subset) > 0:
        found_count += 1
        top_skills = subset.sort_values(by=val_col, ascending=False).head(3)
        skills_str = ", ".join([f"{r[element_col]} ({r[val_col]})" for _, r in top_skills.iterrows()])
        print(f"{soc}: {skills_str}")

print(f"\nTotal careers with O*NET Essential Skills: {found_count} / {len(soc_list)}")
