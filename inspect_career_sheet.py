import pandas as pd
import json

df_career = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='final carrer sheet')
print(f"Total rows in final carrer sheet: {len(df_career)}")
print(f"Columns: {df_career.columns.tolist()}")

# Check for duplicates or empty rows
print("\nNull checks in 'Carrer name':", df_career['Carrer name'].isnull().sum())
print("Value counts > 1 in 'Carrer name':")
vc = df_career['Carrer name'].value_counts()
print(vc[vc > 1])

# Inspect Occupation Data sheet
df_occ = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='Occupation Data')
print(f"\nOccupation Data rows: {len(df_occ)}")
print(f"Occupation Data columns: {df_occ.columns.tolist()}")

# Print sample row representation in utf-8
for idx, row in df_career.head(3).iterrows():
    print(f"\n--- Career {idx}: {row['Carrer name']} ({row['O*NET-SOC Code']}) ---")
    print(f"Skills: {str(row['Skill'])[:120]}...")
    print(f"Tools: {str(row['Software/Tools'])[:120]}...")
    print(f"Roadmap: {str(row['Carrer roadmap'])[:150]}...")
    print(f"Salary: {row['Median salary']}, Outlook: {row['Job outlook']}")
