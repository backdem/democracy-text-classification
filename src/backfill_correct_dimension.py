import pandas as pd
from datetime import datetime
import sys



corpus_file = '../../data/democracy_reports_corpus_merged_wbacksliding_040724.csv'

df = pd.read_csv(corpus_file)

input_name = 'correct_dimension'
higher_level_column_name = 'dimension0'
r1_col = 'dimension0_r1'
r2_col = 'dimension0_r2'
r3_col = 'dimension0_r3'

count_correct = df[input_name].notna().sum()
print(f"Count correct_dimension: {count_correct}")
count_r1 = df[r1_col].notna().sum()
print(f"Count r1: {count_r1}")
count_r2 = df[r2_col].notna().sum()
print(f"Count r2: {count_r2}")
count_r3 = df[r3_col].notna().sum()
print(f"Count r3: {count_r3}")

df_out = df.copy()


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


df_out[input_name].fillna(df_out[r1_col], inplace=True)
df_out[input_name].fillna(df_out[r2_col], inplace=True)
df_out[input_name].fillna(df_out[r3_col], inplace=True)
df_out[higher_level_column_name] = df_out[input_name].apply(higher_dimension)

count_correct = df_out[input_name].notna().sum()
print(f"Count correct_dimension: {count_correct}")
count_dim0 = df_out[higher_level_column_name].notna().sum()
print(f"Count dimension0: {count_dim0}")

file_name = datetime.now().strftime('../../data/democracy_reports_corpus_%d%m%y')

# Save merged CSV 
print(f"Saving {file_name}.csv")
df_out.to_csv(f"{file_name}.csv", index=False)
print(f"Saving {file_name}.xlsx")
df_out.to_excel(f"{file_name}.xlsx", index=False)

print(f"Saved files: {file_name}.csv|.xlsx")

