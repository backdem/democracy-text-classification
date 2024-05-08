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
df_out['dimension1_r2'] = None
df_out['dimension2_r2'] = None
df_out['backsliding_r2'] = None
df_out['dimension1_r3'] = None
df_out['dimension2_r3'] = None
df_out['backsliding_r3'] = None
#df_filtered = df[df['dimension1'].notnull()]
#sample_rows = df_filtered.sample(100)

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
            df_out.loc[i1, "dimension1_r2"] = df_2.loc[i2, "dimension1"]
            df_out.loc[i1, "dimension2_r2"] = df_2.loc[i2, "dimension2"]
            df_out.loc[i1, "backsliding_r2"] = df_2.loc[i2, "backsliding"]
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
                df_out.loc[i1, "dimension1_r2"] = df_2.loc[i2, "dimension1"]
                df_out.loc[i1, "dimension2_r2"] = df_2.loc[i2, "dimension2"]
                df_out.loc[i1, "backsliding_r2"] = df_2.loc[i2, "backsliding"]
        if not match:
            print(f"[NO MATCH 2] {row2['sentence']}")
            
            # if d1 == d2:
            #     agree += 1
            #     y1.append(d1)
            #     y2.append(d2)
            #
            #     
            # if d1 != d2 and not pd.isna(d1):
            #     #print(f'match: {index} {i1}')
            #     #print(f'dimension1: {row1["dimension1"]} :: {row2["dimension1"]}')
            #     #print()
            #     disagree += 1
            #     y1.append(d1)
            #     y2.append(d2)
#         #     s2_1 = row['sentence']
    # ss = row['sentence']
    # sr = df_2.iloc[index]['sentence']
    # if sr != ss:
    #     print(ss)
    #     print(sr)
    #     print(index)
    #     break
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
            df_out.loc[i1, "dimension1_r3"] = df_3.loc[i3, "dimension1"]
            df_out.loc[i1, "dimension2_r3"] = df_3.loc[i3, "dimension2"]
            df_out.loc[i1, "backsliding_r3"] = df_3.loc[i3, "backsliding"]
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
                df_out.loc[i1, "dimension1_r3"] = df_3.loc[i3, "dimension1"]
                df_out.loc[i1, "dimension2_r3"] = df_3.loc[i3, "dimension2"]
                df_out.loc[i1, "backsliding_r3"] = df_3.loc[i3, "backsliding"]
        if not match:
            print(f"[NO MATCH 3] {row3['sentence']}")
            
            # if d1 == d2:
            #     agree += 1
            #     y1.append(d1)
            #     y2.append(d2)
            #
            #     
            # if d1 != d2 and not pd.isna(d1):
            #     #print(f'match: {index} {i1}')
            #     #print(f'dimension1: {row1["dimension1"]} :: {row2["dimension1"]}')
            #     #print()
            #     disagree += 1
            #     y1.append(d1)
            #     y2.append(d2)


# print()
# ck = cohen_kappa_score(y1, y2)
# print(ck)

# Save merged CSV 
df_out.to_csv("result_merged.csv", index=False)

df = pd.read_csv("result_merged.csv")
df_filtered = df[df['dimension1_r3'].notnull()]
sample_rows = df_filtered.sample(10)
for index, row in sample_rows.iterrows():
    print(f"Row {index}:")
    # Iterate through the columns
    for column_name, column_value in row.items():
        print(f"{column_name}: {column_value}")
    print()  # Print an empty line for separation


# # Find where the mismatch starts
# offset = 0
# offset_list = []
# for index, row in df_1.iterrows():
#
#     other_row = df_2.iloc[index + offset]
#     s1 = row['sentence']
#     s2 = other_row['sentence']
#     if s1 != s2:
#         offset += 1
#         offset_list.append((index, offset))
#
#         print(index)
#         print(s1)
#         print(s2)
#         # print('------------')
#         # offset_rows = df_2.iloc[index-1:index+100]
#         # for i2, row in offset_rows.iterrows():
#         #     s2_1 = row['sentence']
#         #     if (s2_1 == s1):
#         #         print(f'[{i2}] {s2_1}')
#         # break

# #random_row_no = random.randint(0, num_rows_1)
# random_row_no = 10
#
# start = random_row_no - 3
# stop = random_row_no + 1
#
# print(f'selecting row {random_row_no}')
#
# #row_1_at_n = df_1.iloc[random_row_no]
# #row_2_at_n = df_2.iloc[random_row_no]
# #rows_1 = df_1.iloc[start:stop]
# #rows_2 = df_2.iloc[start:stop]
# rows_1 = df_1.iloc[random_row_no:random_row_no+1]
# rows_2 = df_2.iloc[random_row_no+2:random_row_no+3]
#
#
# for index, row in rows_1.iterrows():
#     print(f"Row {index}:")
#     for column_name, column_value in row.items():
#         print(f"{column_name}: {column_value}")
#     print()  # Print an empty line for separation
#
# print('----')
#
# for index, row in rows_2.iterrows():
#     print(f"Row {index}:")
#     for column_name, column_value in row.items():
#         print(f"{column_name}: {column_value}")
#     print()  # Print an empty line for separation
#
#
#
# # Iterate through the rows
# #for index, row in sample_rows.iterrows():
# #    print(f"Row {index}:")
# #    # Iterate through the columns
# #    for column_name, column_value in row.items():
# #        print(f"{column_name}: {column_value}")
# #    print()  # Print an empty line for separation

