import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

excel_path = 'data/Technical_Careers_ONET.xlsx'
df = pd.read_excel(excel_path, sheet_name='final carrer sheet').dropna(subset=['Carrer name'])

all_skills = set()
all_tools = set()

for idx, row in df.iterrows():
    skills = str(row['Skill']).split(',')
    for s in skills:
        s_clean = s.strip()
        if s_clean and s_clean != 'nan':
            all_skills.add(s_clean)
            
    tools = str(row['Software/Tools']).split(',')
    for t in tools[:10]: # check first 10 tools
        t_clean = t.strip()
        if t_clean and t_clean != 'nan':
            all_tools.add(t_clean)

print(f"Total distinct skill keywords extracted: {len(all_skills)}")
print("Sample skills:", sorted(list(all_skills))[:20])
print(f"\nTotal sample tools extracted: {len(all_tools)}")
print("Sample tools:", sorted(list(all_tools))[:20])
