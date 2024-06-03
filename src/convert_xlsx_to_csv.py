import pandas as pd 
import os
import sys


xlsx_file = sys.argv[1]
csv_file = sys.argv[2]

if not os.path.exists(xlsx_file):
    print(f'File not found {xlsx_file}.')
    sys.exit(1)

df = pd.read_excel(xlsx_file)
df.to_csv(csv_file, index=False)
print(f'Done converting {xlsx_file} to {csv_file}.')

