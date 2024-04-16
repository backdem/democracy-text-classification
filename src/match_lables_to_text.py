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
with open(label_file, 'r') as file:
    for line in file:
        # Substitute the old section column of form "[something, eomthing else, etc]"
        # for easy comma splitting later
        line = re.sub(r'\[.*?\]','QWERTY', line.strip())
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

        if(len(country_year_source) < 3):
            # Something went wrong save it somewhere else
            print(f"[WARNING 1] line: {line} has no country_year_source.")
            row['sentence'] = text
        else:
            row['sentence'] = sentence
            row['country'] = country_year_source[0]
            row['year'] = country_year_source[1]
            row['source'] = country_year_source[2]

        if len(labels) < 10:
            #print(f"[WARNING 2] line: {line} has only {len(labels)} labels.")
            row['dimension1'] = ''
            row['dimension2'] = ''
            row['dimension3'] = ''
            row['dimension4'] = ''
            row['backsliding'] = ''
            row['cat_4_sentence_nuance'] = ''
            row['comments'] = ''
            row['undefined0'] = ''
            row['undefined1'] = ''
            row['consensus'] = ''
        else:
            row['dimension1'] = labels[0]
            row['dimension2'] = labels[1]
            row['dimension3'] = labels[2]
            row['dimension4'] = labels[3]
            row['backsliding'] = labels[4]
            row['cat_4_sentence_nuance'] = labels[5]
            row['comments'] = labels[6]
            row['undefined0'] = labels[7]
            row['undefined1'] = labels[8]
            row['consensus'] = labels[9]


        if(len(country_year_source) < 3):
            # Something went wrong save it somewhere else
            other_data.append(row)
        else:
            data.append(row)

df_good = pd.DataFrame(data)
df_bad = pd.DataFrame(other_data)

df_good.to_csv("result.csv", index=False)
df_bad.to_csv("result_bad.csv", index=False)

df = pd.read_csv('result.csv')
print(df.sample(10))

