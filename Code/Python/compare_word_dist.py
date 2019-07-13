"""
Compare word distribution of CCP imporving refactors and those that don't.
"""

import pandas as pd
import re

DATA_PATH = '/Users/iamit/Documents/PhD/goto/data/'

def tokanize_commit_df(df):

    tokanization = []
    for _, i in df.iterrows():
        tokens = re.split('[_ \n\t\r\.!?;:\"\'/-]', i['message'].lower())
        for j in tokens:
            tokanization.append((i.repo_name, i.commit, j))

    tokanization_df = pd.DataFrame(tokanization
                                   , columns=['repo_name', 'commit', 'token'])

    return tokanization_df

def tokanize_commit_file(file):
    df = pd.read_csv(file)


    return tokanize_commit_df(df)


def compare_word_dist_files(positive_path
                      , negative_path):
    pos_df = tokanize_commit_file(positive_path)
    pos_df['positive'] = 1
    neg_df = tokanize_commit_file(negative_path)
    neg_df['positive'] = 0

    tokens = pd.concat([pos_df, neg_df])

    token_agg = tokens.groupby(['token'], as_index=False).agg({'commit' : 'nunique'
                                                               , 'positive' : 'mean'})

    return token_agg



def compare_word_dist(positive_sample
                      , negative_samples):
    pos_df = tokanize_commit_df(positive_sample)
    pos_df['positive'] = 1
    neg_df = tokanize_commit_df(negative_samples)
    neg_df['positive'] = 0

    tokens = pd.concat([pos_df, neg_df])

    token_agg = tokens.groupby(['token'], as_index=False).agg({'commit' : 'nunique'
                                                               , 'positive' : 'mean'})

    return token_agg



def compare_word_dist_files(positive_file
                      , negative_file):
    positive_sample = pd.read_csv(positive_file)
    negative_samples = pd.read_csv(negative_file)

    return compare_word_dist(positive_sample
                      , negative_samples)

def agg_by_message(df):
    agg = df.groupby(['message'], as_index=False).agg({'commit' : 'max'
                    , 'author_date' : 'max'
                    , 'ccp_diff' : 'max'
                    , 'coupling_diff' : 'max'
                    , 'coupling_no_test_diff' : 'max'})
    agg['repo_name'] = ''

    return agg



if __name__ == "__main__":
    word_dist = compare_word_dist_files(DATA_PATH + 'ccp_improving_refactors.csv'
                                  , DATA_PATH + 'ccp_not_improving_refactors.csv')
    print "negative"
    print word_dist[(word_dist.commit > 20) & (word_dist.positive < 0.3)].sort_values(['positive', 'commit'], ascending=[True,False])
    print "positive"
    print word_dist[(word_dist.commit > 20) & (word_dist.positive > 0.7)].sort_values(['positive', 'commit'], ascending=[False,False])
    word_dist.to_csv(DATA_PATH + 'ccp_changing_tokens.csv')