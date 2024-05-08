import pandas as pd
import hashlib
import re
import sys
label_file = '../../data/democracy_reports_corpus_annelisa_9.csv'
column_name = 'sentence,section,country,year,source'
#['dimension1', 'dimension2', 'dimension3', 'dimension 4', 'backsliding', 'cat 4 sentence nuance', 'comments + possible need to be changed bc of changes in labeling instructions (marked: ?)', '', '', 'Group: sentences we discussed, X for no consensus, O for new consensus', '', '', '', '', '', '', '', '', '']
i = 0
data = []
other_data = []
typos = { 'ambigous': 'ambiguous', 'electioms': 'elections'}
def fix(l):
    # {'direct democracy ', 'ambiguous ', 'ambigous', 'liberal rights', 'electoral', 'elections ', 'electioms', 'media ', 'opo', 'participatory', ' ambiguous'}
    if l.strip() in typos:
        return typos[l]
    else:
        return l.strip()

with open(label_file, 'r') as file:
    for _line in file:
        # Substitute the old section column of form "[something, eomthing else, etc]"
        matched_strs = []
        # Save matched string to replace later.
        def save_match(match):
            # Save the matched substring to a list
            matched_strs.append(match.group(0))
            # You can perform additional processing here if needed
            return 'QWERTY'
        # for easy comma splitting later
        line = re.sub(r'\[.*?\]', save_match, _line.strip())
        row = {}
        i += 1
        # Skip header line
        if i == 1:
            continue
        # First split by ';'
        parts = line.split(';')

        # Find where the year is mentioned to be used as the
        # chop off point
        index_of_year = 0
        for c, e in enumerate(parts):
            if re.search(r'\d{4}', e):
                index_of_year = c
        no = len(parts) - index_of_year - 1

        # Remove the labels
        labels = parts[-no:]

        # Rejoin the text (it may have had the delimiter ';' as part od string)
        text = ';'.join(parts[:-no])

        # Split by comma
        text_parts = text.split(",")
        # Get the old label columns of country, year and source
        country_year_source = text_parts[-3:]
        # Rejoin the rest to form the old sentence
        sentence = ','.join(text_parts[:-4])
        # Replace back QWERTY tokens
        while 'QWERTY' in sentence:
            #print(f"[WARNING 3] Invalid token in {sentence}.")
            replacement = matched_strs.pop(0)
            sentence = re.sub('QWERTY', replacement, sentence, count=1)
            #print(f"<--{_line.strip()}")
            #print(f"-->{sentence}")

        if(len(country_year_source) < 3):
            # Something went wrong save it somewhere else
            print(f"[WARNING 1] line: {line} has no country_year_source.")
            row['sentence'] = text
        else:
            row['sentence'] = sentence
            row['country'] = country_year_source[0]
            row['year'] = country_year_source[1]
            row['source'] = country_year_source[2]

        if len(labels) < 9:
            #print(f"[WARNING 2] line: {line} has only {len(labels)} labels.")
            row['dimension1'] = None
            row['dimension2'] = None
            row['backsliding'] = None
            row['cat_4_sentence_nuance'] = None
            row['start_idea'] = None
            row['comments'] = None
            row['undefined0'] = None
            row['undefined1'] = None
            row['consensus'] = None
        else:
            row['dimension1'] = fix(labels[0])
            row['dimension2'] = fix(labels[1])
            row['backsliding'] = labels[2]
            row['cat_4_sentence_nuance'] = labels[3]
            row['start_idea'] = labels[4]
            row['comments'] = labels[5]
            row['undefined0'] = labels[6]
            row['undefined1'] = labels[7]
            row['consensus'] = labels[8]


        if(len(country_year_source) < 3):
            # Something went wrong save it somewhere else
            other_data.append(row)
        else:
            data.append(row)

df_good = pd.DataFrame(data)
df_bad = pd.DataFrame(other_data)

df_good.to_csv("result_r1.csv", index=False)
df_bad.to_csv("result_bad_r1.csv", index=False)

df = pd.read_csv('result_r1.csv')
sample_rows = df.sample(10)

# Iterate through the rows
for index, row in sample_rows.iterrows():
    print(f"Row {index}:")
    # Iterate through the columns
    for column_name, column_value in row.items():
        print(f"{column_name}: {column_value}")
    print()  # Print an empty line for separation

