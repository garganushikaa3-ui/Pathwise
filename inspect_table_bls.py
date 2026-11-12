import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df_bls = pd.read_excel('data/Technical_Careers_ONET.xlsx', sheet_name='Table 1.2')
print("Table 1.2 shape:", df_bls.shape)
print("First 15 rows of Table 1.2:")
for idx, row in df_bls.head(15).iterrows():
    vals = [str(x) for x in row.values if pd.notnull(x)]
    print(f"Row {idx}: {' | '.join(vals[:6])}")
