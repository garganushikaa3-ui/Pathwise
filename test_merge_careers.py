import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

# Load sheets
excel_path = 'data/Technical_Careers_ONET.xlsx'
df_final = pd.read_excel(excel_path, sheet_name='final carrer sheet').dropna(subset=['Carrer name'])
df_occ = pd.read_excel(excel_path, sheet_name='Occupation Data')
df_bls = pd.read_excel(excel_path, sheet_name='Table 1.2')

# Setup BLS lookup by 6-digit SOC code (e.g., 15-1252 from 15-1252.00)
bls_headers = df_bls.iloc[0].tolist()
df_bls_data = df_bls.iloc[1:].copy()
df_bls_data.columns = bls_headers

# Strip whitespace
df_bls_data['soc_clean'] = df_bls_data['2025 National Employment Matrix code'].astype(str).str.strip()

print(f"Total careers in final sheet: {len(df_final)}")

# Map descriptions
occ_map = dict(zip(df_occ['O*NET-SOC Code'].astype(str).str.strip(), df_occ['Description']))

matched = 0
for idx, row in df_final.iterrows():
    soc = str(row['O*NET-SOC Code']).strip()
    soc_prefix = soc[:7] if len(soc) >= 7 else soc  # e.g., '15-1252'
    name = row['Carrer name']
    
    # Check BLS match
    bls_row = df_bls_data[df_bls_data['soc_clean'] == soc_prefix]
    wage = "Data not available"
    growth = "Data not available"
    edu = "Data not available"
    exp = "Data not available"
    
    if len(bls_row) > 0:
        matched += 1
        wage = bls_row.iloc[0]['Median annual wage, dollars, 2025']
        growth = bls_row.iloc[0]['Employment change, percent, 2025–35']
        edu = bls_row.iloc[0]['Typical education needed for entry']
        exp = bls_row.iloc[0]['Work experience in a related occupation']
    
    print(f"{name} ({soc}) -> Wage: {wage}, Growth: {growth}%, Edu: {edu}")

print(f"Matched with BLS: {matched} / {len(df_final)}")
