import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df_bls = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='Table 1.2')
row0 = df_bls.iloc[0].tolist()
for i, col in enumerate(row0):
    print(f"Col {i}: {col}")
