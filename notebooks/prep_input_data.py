import pandas as pd
# corpus_file = '../../data/democracy_reports_corpus_annelisa_9_fixed.csv'


def get_labelled_data(corpus_file, all=False, column='dimension1'):
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

    return df_new

def get_vectorized_labelled_data(corpus_file, column='dimension1'):

    # Create label vector column
    # Label sentences with topics, producing 
    # a masked label vector of the form [0, 0, 0, 0, 0, 1] where the 
    # indicies match topics ['ambiguous', 'electoral', 'liberal institutions', 'liberal rights', 'media', 'participatory']
    def generate_label_vector(row, l):
        label = row[column]
        return [int(l == label) for l in labels]
        
    df_labelled = get_labelled_data(corpus_file, all=False, column=column)
    labels = sorted(df_labelled[column].dropna().unique())
    df_labelled_new = df_labelled.copy()
    df_labelled_new['label_vector'] = df_labelled_new.apply(generate_label_vector, l=labels, axis=1)
    return df_labelled_new
