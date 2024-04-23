import pandas as pd

def group_on_idea(df, max_len=510):

    idea = -1
    s_len = 0
    label = None
    accumulator = []
    new_rows = []
    columns = ['sentence', 'country', 'year', 'source', 'dimension1', 'dimension2', 'backsliding']
    def create_row(accumulator):
        # Create new row by reducing accumulator
        new_sentence = ''
        new_row = []
        fr = accumulator[0]
        for r in accumulator:
            if(isinstance(r['sentence'], float)):
               #print(r['sentence'])
               continue
            new_sentence += str(r['sentence'])
        new_row.append(new_sentence.strip())
        new_row.append(fr['country'])
        new_row.append(fr['year'])
        new_row.append(fr['source'])
        new_row.append(fr['dimension1'])
        new_row.append(fr['dimension2'])
        new_row.append(fr['backsliding'])
        return new_row

    def strip_row(fr):
        new_row = []
        new_row.append(fr['sentence'])
        new_row.append(fr['country'])
        new_row.append(fr['year'])
        new_row.append(fr['source'])
        new_row.append(fr['dimension1'])
        new_row.append(fr['dimension2'])
        new_row.append(fr['backsliding'])
        return new_row


    for index, row in df.iterrows():
        if(isinstance(row['sentence'], float)):
           #print(r['sentence'])
           continue
        if ((idea == 1) and (row['dimension1'] == label)):
            curr_len = s_len + len(row['sentence'])
            if(curr_len >= max_len):
                if(len(accumulator) > 0):
                    new_row = create_row(accumulator)
                    new_rows.append(new_row)
                    accumulator = []
                    s_len = 0
                else:
                    new_rows.append(strip_row(row))
                    s_len = 0
            else:
                accumulator.append(row)
                s_len += curr_len
            continue
        if ((idea == 1) and (row['dimension1'] != label)):
            if(len(accumulator) > 0):
                new_row = create_row(accumulator)
                new_rows.append(new_row)
                accumulator = []
            idea = -1
            label = None
            continue
        if row['start_idea'] == 1:
            if(len(accumulator) > 0):
                new_row = create_row(accumulator)
                new_rows.append(new_row)
                accumulator = []
            idea = 1
            label = row['dimension1']
            accumulator.append(row)
            s_len += len(row['sentence'])
            continue
        new_rows.append(strip_row(row))
    return pd.DataFrame(new_rows, columns=columns)


def get_labelled_data(corpus_file, all=False, column='dimension1', group_by_idea=False, use_higher_dimensions=True):
    # Read csv file into Dataframe
    df = pd.read_csv(corpus_file, dtype={'year': str},comment='#')
    if (all == True):
        df_labelled = df 
    else:
        # Filter for labelled data
        df_labelled = df[df['dimension1'].notnull()] 
    # Print sample rows
    #print(df_labelled.sample(5))

    # Convert column to numeric
    def convert_to_int(x):
        try:
            # Combine class 4 (ambivalent) with class 0 (ambiguous)
            y = int(x)
            if y == 4:
                return int(0)
            else:            
                return int(x)  # For example, doubling the values after converting to int
        except ValueError:
            return None

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

    # Get label names
    labels = df_labelled[column].dropna().unique()
    # print(f'Found labels: {labels}')
    # Fix typos in labels
    def find_replace_in_column(df, column_name, string_to_match, new_value):
        df.loc[df[column_name] == string_to_match, column_name] = new_value
        return df
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'media ', 'media')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'electoral?', 'electoral')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'liberal rights?', 'liberal rights')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'liberal rights ', 'liberal rights')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'liberal righ', 'liberal rights')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'media l', 'media')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'electioms', 'elections')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'ambigous', 'ambiguous')
    df_labelled = find_replace_in_column(df_labelled, 'dimension1', 'elections ', 'elections')
    df_new = df_labelled.copy()
    df_new['backsliding'] = df_new['backsliding'].apply(convert_to_int)
    if group_by_idea:
        df_new = group_on_idea(df_new)
    if use_higher_dimensions:
        df_new['dimension0'] = df_new['dimension1'].apply(higher_dimension)

    return df_new

def get_vectorized_labelled_data(corpus_file, column='dimension1', group_by_idea=False, use_higher_dimensions=True):

    # Create label vector column
    # Label sentences with topics, producing 
    # a masked label vector of the form [0, 0, 0, 0, 0, 1] where the 
    # indicies match topics ['ambiguous', 'electoral', 'liberal institutions', 'liberal rights', 'media', 'participatory']
    def generate_label_vector(label, labels):
        #label = row[column]
        return [int(l == label) for l in labels]
        
    df_labelled = get_labelled_data(corpus_file, all=False, column=column, group_by_idea=group_by_idea)
    labels = []
    if use_higher_dimensions:
        labels = sorted(df_labelled['dimension0'].dropna().unique())
        df_labelled_new = df_labelled.copy()
        df_labelled_new['label_vector'] = df_labelled_new['dimension0'].apply(generate_label_vector, labels=labels)
    else:
        labels = sorted(df_labelled[column].dropna().unique())
        df_labelled_new = df_labelled.copy()
        df_labelled_new['label_vector'] = df_labelled_new[column].apply(generate_label_vector, labels=labels)
    return df_labelled_new


# Test
corpus_file = '../../data/democracy_reports_corpus_annelisa_9_fixed.csv'
df = get_vectorized_labelled_data(corpus_file)
#df = get_labelled_data(corpus_file, group_by_idea=True)
#df['sentence_len'] = df['sentence'].dropna().apply(len)
#max_l = df['sentence_len'].max()
#print(max_l)
df.to_csv('./AAAAtext.csv', index=False)
