import pandas as pd
import random
from sklearn.metrics import cohen_kappa_score
file_2 = './result_r2.csv'
file_1 = './result_r1.csv'
file_3 = './result_r3.csv'
df_1 = pd.read_csv(file_1)
df_2 = pd.read_csv(file_2)
df_3 = pd.read_csv(file_3)

# Compare labels

labels_1 = df_1['dimension1'].unique()
labels_2 = df_2['dimension1'].unique()
labels_3 = df_3['dimension1'].unique()

print(f'Labels R1: {labels_1}')
print(f'Labels R2: {labels_2}')
print(f'Labels R3: {labels_3}')

intersection = set(labels_1) & set(labels_2) & set(labels_3)
inverse = (set(labels_1) | set(labels_2) | set(labels_3)) - intersection

print(inverse)
#df_filtered = df[df['dimension1'].notnull()]
#sample_rows = df_filtered.sample(100)

df_filtered = df_2[df_2['dimension1'] == 'opo']
print(df_filtered)

num_rows_1 = df_1.shape[0]
num_rows_2 = df_2.shape[0]
num_rows_3 = df_3.shape[0]

print(f'{file_1} rows {num_rows_1}')
print(f'{file_2} rows {num_rows_2}')
print(f'{file_3} rows {num_rows_3}')

# labelled_df_2 = df_2.loc[df_2['dimension1'].notnull()]
#
# disagree = 0
# agree = 0
# y1 = []
# y2 = []
# for index, row2 in labelled_df_2.iterrows():
#     start = index - 10 
#     stop = index + 10
#     df_1_rows = df_1.iloc[start:stop]
#     for i1, row1 in df_1_rows.iterrows():
#         s1 = row1['sentence']
#         s2 = row2['sentence']
#         if s1 == s2:
#             d1 = row1['dimension1']
#             d2 = row2['dimension1']
#             
#             if d1 == d2:
#                 agree += 1
#                 y1.append(d1)
#                 y2.append(d2)
#
#                 
#             if d1 != d2 and not pd.isna(d1):
#                 print(f'match: {index} {i1}')
#                 print(f'dimension1: {row1["dimension1"]} :: {row2["dimension1"]}')
#                 print()
#                 disagree += 1
#                 y1.append(d1)
#                 y2.append(d2)
# #         #     s2_1 = row['sentence']
#     # ss = row['sentence']
#     # sr = df_2.iloc[index]['sentence']
#     # if sr != ss:
#     #     print(ss)
#     #     print(sr)
#     #     print(index)
#     #     break
#
#
# print()
# ck = cohen_kappa_score(y1, y2)
# print(ck)
#
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

