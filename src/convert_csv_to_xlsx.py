
import pandas as pd 
import os
import sys


xlsx_file = sys.argv[2]
csv_file = sys.argv[1]

if not os.path.exists(csv_file):
    print(f'File not found {csv_file}.')
    sys.exit(1)

df = pd.read_csv(csv_file)
df.to_excel(xlsx_file, index=False)
print(f'Done converting {csv_file} to {xlsx_file}.')
