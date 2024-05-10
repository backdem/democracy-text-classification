import pandas as pd
import random
import sys
from sklearn.metrics import cohen_kappa_score
file_1 = './result_r1.csv'
file_2 = './result_r2.csv'
file_3 = './result_r3.csv'
df_1 = pd.read_csv(file_1)
df_2 = pd.read_csv(file_2)
df_3 = pd.read_csv(file_3)
df_out = df_1.copy()
df_out['dimension0_r2'] = None
df_out['dimension1_r2'] = None
df_out['dimension2_r2'] = None
df_out['backsliding_r2'] = None
df_out['dimension0_r3'] = None
df_out['dimension1_r3'] = None
df_out['dimension2_r3'] = None
df_out['backsliding_r3'] = None
#df_filtered = df[df['dimension1'].notnull()]
#sample_rows = df_filtered.sample(100)

num_rows_1 = df_1.shape[0]
num_rows_2 = df_2.shape[0]

print(f'{file_1} rows {num_rows_1}')
print(f'{file_2} rows {num_rows_2}')
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

# Merge r2 into r1
labelled_df_2 = df_2.loc[df_2['dimension1'].notnull()]
for i2, row2 in labelled_df_2.iterrows():
    start = max(i2 - 10,0) 
    stop = min(i2 + 10, df_1.shape[0])
    df_1_rows = df_1.iloc[start:stop]
    match = False
    for i1, row1 in df_1_rows.iterrows():
        s1 = row1['sentence']
        s2 = row2['sentence']
        if s1 == s2:
            match = True
            #print(f"[TRUE] {s2}")
            d1 = row1['dimension1']
            d2 = row2['dimension1']
            df_out.loc[i1, "dimension0_r2"] = higher_dimension(df_2.loc[i2, "dimension1"])
            df_out.loc[i1, "dimension1_r2"] = df_2.loc[i2, "dimension1"]
            df_out.loc[i1, "dimension2_r2"] = df_2.loc[i2, "dimension2"]
            df_out.loc[i1, "backsliding_r2"] = df_2.loc[i2, "backsliding"]
            df_out.loc[i1, "start_idea_r2"] = df_2.loc[i2, "start_idea"]
        #else:
        #    print(f"[FALSE] {s1} ::: {s2}")
    if not match:
        #print(f"[NO MATCH 2] {row2['sentence']}")
        for i1, row1 in df_1_rows.iterrows():
            s1 = row1['sentence']
            s2 = row2['sentence']
            if compare_first_n_words(s1, s2):
                match = True
                #print(f"[TRUE on 2nd try] {s2} ::: {s1}")
                d1 = row1['dimension1']
                d2 = row2['dimension1']
                df_out.loc[i1, "dimension0_r2"] = higher_dimension(df_2.loc[i2, "dimension1"])
                df_out.loc[i1, "dimension1_r2"] = df_2.loc[i2, "dimension1"]
                df_out.loc[i1, "dimension2_r2"] = df_2.loc[i2, "dimension2"]
                df_out.loc[i1, "backsliding_r2"] = df_2.loc[i2, "backsliding"]
                df_out.loc[i1, "start_idea_r2"] = df_2.loc[i2, "start_idea"]
        if not match:
            print(f"[NO MATCH 2] {row2['sentence']}")
            
# Merge r3 into r1
labelled_df_3 = df_3.loc[df_3['dimension1'].notnull()]
for i3, row3 in labelled_df_3.iterrows():
    start = max(i3 - 10,0) 
    stop = min(i3 + 10, df_1.shape[0])
    df_1_rows = df_1.iloc[start:stop]
    match = False
    for i1, row1 in df_1_rows.iterrows():
        s1 = row1['sentence']
        s3 = row3['sentence']
        if s1 == s3:
            d1 = row1['dimension1']
            d3 = row2['dimension1']
            df_out.loc[i1, "dimension0_r3"] = higher_dimension(df_3.loc[i3, "dimension1"])
            df_out.loc[i1, "dimension1_r3"] = df_3.loc[i3, "dimension1"]
            df_out.loc[i1, "dimension2_r3"] = df_3.loc[i3, "dimension2"]
            df_out.loc[i1, "backsliding_r3"] = df_3.loc[i3, "backsliding"]
            df_out.loc[i1, "start_idea_r3"] = df_3.loc[i3, "start_idea"]
    if not match:
        #print(f"[NO MATCH 2] {row2['sentence']}")
        for i1, row1 in df_1_rows.iterrows():
            s1 = row1['sentence']
            s3 = row3['sentence']
            if compare_first_n_words(s1, s3):
                match = True
                #print(f"[TRUE on 2nd try] {s2} ::: {s1}")
                d1 = row1['dimension1']
                d3 = row3['dimension1']
                df_out.loc[i1, "dimension0_r3"] = higher_dimension(df_3.loc[i3, "dimension1"])
                df_out.loc[i1, "dimension1_r3"] = df_3.loc[i3, "dimension1"]
                df_out.loc[i1, "dimension2_r3"] = df_3.loc[i3, "dimension2"]
                df_out.loc[i1, "backsliding_r3"] = df_3.loc[i3, "backsliding"]
                df_out.loc[i1, "start_idea_r3"] = df_3.loc[i3, "start_idea"]
        if not match:
            print(f"[NO MATCH 3] {row3['sentence']}")

# Drop unacessary columns
df_out = df_out.drop(columns=['undefined0', 'undefined1', 'cat_4_sentence_nuance', 'consensus', 'comments'])
# Rename r1 columns
df_out = df_out.rename(columns={'dimension1': 'dimension1_r1', 'dimension2': 'dimension2_r1', 'backsliding':'backsliding_r1', 'start_idea': 'start_idea_r1'})
df_out['dimension0_r1'] = df_out['dimension1_r1'].apply(higher_dimension)

# Save merged CSV 
df_out.to_csv("result_merged.csv", index=False)
df_out.to_excel('result_merged.xlsx', index=False)

df = pd.read_csv("result_merged.csv")
df_filtered = df[df['dimension1_r3'].notnull() | df['dimension1_r1'].notnull() | df['dimension1_r2'].notnull()]
df_filtered_3 = df[df['dimension1_r3'].notnull() & df['dimension1_r1'].notnull() & df['dimension1_r2'].notnull()]
sample_rows = df_filtered.sample(1)
for index, row in sample_rows.iterrows():
    print(f"Row {index}:")
    # Iterate through the columns
    for column_name, column_value in row.items():
        print(f"{column_name}: {column_value}")
    print()  # Print an empty line for separation

print(f"all rows: {df.shape[0]}, at least one label: {df_filtered.shape[0]}, 3 labels: {df_filtered_3.shape[0]}")
