import pandas as pd
# corpus_file = '../../data/democracy_reports_corpus_annelisa_9_fixed.csv'


def get_labelled_data(corpus_file, all=False):
    # Read csv file into Dataframe
    df = pd.read_csv(corpus_file, dtype={'year': str},comment='#')
    if (all == True):
        df_labelled = df 
    else:
        # Filter for labelled data
        df_labelled = df[(df['dimension1'].notnull()) | (df['dimension2'].notnull()) | (df['dimension3'].notnull()) | (df['dimension4'].notnull())] 
    # Print sample rows
    #print(df_labelled.sample(5))

    # Get label names
    labels = df_labelled['dimension1'].unique()
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
    return df_labelled

def get_vectorized_labelled_data(corpus_file):

    # Create label vector column
    # Label sentences with topics, producing 
    # a masked label vector of the form [0, 0, 0, 0, 0, 1] where the 
    # indicies match topics ['ambiguous', 'electoral', 'liberal institutions', 'liberal rights', 'media', 'participatory']
    def generate_label_vector(row, l):
        label = row['dimension1']
        return [int(l == label) for l in labels]
        
    df_labelled = get_labelled_data(corpus_file)
    labels = df_labelled['dimension1'].dropna().unique()
    df_labelled_new = df_labelled.copy()
    df_labelled_new['label_vector'] = df_labelled_new.apply(generate_label_vector, l=labels, axis=1)
    return df_labelled_new
