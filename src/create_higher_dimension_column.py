i port pandas as pd
import random
import sys
from sklearn.metrics import cohen_kappa_score
corpus_file = '../../data/democracy_reports_corpus_merged_210524_2.csv'
output_file_csv = '../../data/democracy_reports_corpus_merged_040624.csv'
output_file_xlsx = '../../data/democracy_reports_corpus_merged_040624.xlsx'
input_col = "correct dimension"
df = pd.read_csv(corpus_file)
def higher_dimension(x):
    if x == 'elections' or x == 'political competition' or x == 'electoral': 
        return 'electoral'
    if x == 'civil society' or x == 'direct democracy' or x == 'open government' or x == 'participatory': 
        return 'participatory'
    if x == 'media': 
        return 'media'
    if x == 'liberal institutions' or x == 'freedoms' or x == 'equality' or x == 'liberal': 
        return 'liberal'
    return x

def find_replace_in_column(df, column_name, string_to_match, new_value):
    df.loc[df[column_name] == string_to_match, column_name] = new_value
    return df

df = find_replace_in_column(df, input_col, 'ambiquous', 'ambiguous')
df = find_replace_in_column(df, input_col, 'elecoral', 'electoral')


df['dimension0'] = df[input_col].apply(higher_dimension)
df = df.rename(columns={input_col: 'correct_dimension'})

# countries = sorted(df.country.unique())
# print(countries)


# Save merged CSV 
df.to_csv(output_file_csv, index=False)
df.to_excel(output_file_xlsx, index=False)

df = pd.read_csv(output_file_csv)
df_filtered = df[df['dimension0'].notnull()]
sample_rows = df_filtered.sample(1)
for index, row in sample_rows.iterrows():
    print(f"Row {index}:")
    # Iterate through the columns
    for column_name, column_value in row.items():
        print(f"{column_name}: {column_value}")
    print()  # Print an empty line for separation

