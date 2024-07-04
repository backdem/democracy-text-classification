import pandas as pd
import random
import sys
from sklearn.metrics import cohen_kappa_score


file_1 = sys.argv[1]
file_2 = sys.argv[2]
df_1 = pd.read_csv(file_1)
df_2 = pd.read_csv(file_2)

# col_name = 'backsliding_corrected'
col_name = 'correct_backsliding'

# Rename label column 
if 'backsliding corrected' in df_1.columns:
    df_1.rename(columns={'backsliding corrected': col_name}, inplace=True)
if 'backsliding corrected' in df_2.columns:
    df_2.rename(columns={'backsliding corrected': col_name}, inplace=True)
if 'backsliding_corrected' in df_1.columns:
    df_1.rename(columns={'backsliding_corrected': col_name}, inplace=True)
if 'backsliding_corrected' in df_2.columns:
    df_2.rename(columns={'backsliding_corrected': col_name}, inplace=True)

# print(f'columns for {file_1}: {df_1.columns}')
# print(f'columns for {file_2}: {df_2.columns}')
df_out = df_1.copy()

num_rows_1 = df_1.shape[0]
num_rows_2 = df_2.shape[0]

print(f'{file_1} rows {num_rows_1}')
print(f'{file_2} rows {num_rows_2}')

def compare_first_n_words(str1, str2, n=4):
    str1 = str1.lower()
    str2 = str2.lower()
    # Split the strings into words
    words1 = str1.split()
    words2 = str2.split()

    # Take the first 4 words of each string
    first_4_words1 = words1[:n]
    first_4_words2 = words2[:n]

    # Compare the first 4 words
    if first_4_words1 == first_4_words2:
        return True
    else:
        return False

# Merge r2 into r1
labelled_df_2 = df_2.loc[df_2[col_name].notnull()]
labelled_df_1 = df_1.loc[df_1[col_name].notnull()]
for i2, row2 in labelled_df_2.iterrows():
    s2 = row2['sentence']
    s1 = df_out.loc[i2, 'sentence']
    if not compare_first_n_words(s2,s1):
        print(f'WARNING sentences do not match {s1} {s2}')
    df_out.loc[i2, col_name] = df_2.loc[i2, col_name]

df_out[col_name].fillna(df_out['backsliding_r1'], inplace=True)
df_out[col_name].fillna(df_out['backsliding_r2'], inplace=True)
df_out[col_name].fillna(df_out['backsliding_r3'], inplace=True)

# labelled_df_out = df_out.loc[df_out[col_name].notnull()]
# print(f'{labelled_df_1.shape[0]}, {labelled_df_2.shape[0]}, {labelled_df_out.shape[0]}')
#
# labelled_df_out = df_out.loc[df_out[col_name].notnull()]
# print(f'{labelled_df_1.shape[0]}, {labelled_df_2.shape[0]}, {labelled_df_out.shape[0]}')
#

# Check column values
# Known typos
df_out['country'] = df_out['country'].replace({'czech-republic':'czechia'})
df_out['source'] = df_out['source'].replace({'eu_rule_of_law"':'eu_rule_of_law', 'bti"':'bti', 'freedomhouse_freedom-net"':'freedomhouse_freedom-net', 'freedomhouse_nations-transit"':'freedomhouse_nations-transit','freedomhouse_freedom-world"':'freedomhouse_freedom-world',' bti"':'bti', 'greco"':'greco', 'freedomhouse_nations-transitnal capacity and financial sustainability of the civic sector"':'freedomhouse_nations-transit'})
df_out[col_name] = df_out[col_name].replace({83:3})
df_out[col_name] = df_out[col_name].replace({'?':None})
df_out['dimension0'] = df_out['dimension0'].replace({'democracy':None})
df_out[col_name] = df_out[col_name].astype(float)
# print(df_out.columns)
df_out.drop(columns=['Unnamed: 21'], inplace=True)


# Save merged CSV 
df_out.to_csv("result_merged.csv", index=False)
df_out.to_excel('result_merged.xlsx', index=False)

df = pd.read_csv("result_merged.csv")
countries = sorted(df['country'].unique())
years = sorted(df['year'].unique())
sources = sorted(df['source'].unique())
dimension0 = df['dimension0'].unique()
backsliding = df[col_name].unique()
print(f'countries: {countries}')
print(f'years: {years}')
print(f'sources: {sources}')
print(f'dimension0: {dimension0}')
print(f'backsliding {backsliding}')
df_filtered = df[df[col_name].notnull()]
sample_rows = df_filtered.sample(1)
for index, row in sample_rows.iterrows():
    print(f"Row {index}:")
    # Iterate through the columns
    for column_name, column_value in row.items():
        print(f"{column_name}: {column_value}")
    print()  # Print an empty line for separation

print(f"all rows: {df.shape[0]}, backsliding labels: {df_filtered.shape[0]}")
