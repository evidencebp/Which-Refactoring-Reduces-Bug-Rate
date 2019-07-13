"""
Compute the file CCP distribution
"""

import pandas as pd

pd.options.display.max_rows = 200

def estimate_ccp(hr):
    return 1.193*hr - 0.06

def find_value_index(df
                     , val
                     , index_field
                     , val_field):

    prev_val = df.iloc[0][val_field]
    prev_index = df.iloc[0][index_field]
    index = None

    for _, i in df.iterrows():
        if i[val_field] >= val:
            index = i[index_field]
            break
        else:
            prev_val = i[val_field]
            prev_index = i[index_field]

    return index


def analyse_file_hit_dist(dist_file
                           , enhanced_file
                           , valid_enhanced_file):
    df = pd.read_csv(dist_file)
    df = df.sort_values('rhit_rate')
    df['ccp'] = df.rhit_rate.map(lambda x: estimate_ccp(x))
    df = df.assign(files_agg=df.files.cumsum())

    vdf = df[(df.ccp > 0) & (df.ccp <1)]
    vdf = vdf.assign(valid_files_agg=vdf.files.cumsum())

    all_files = df.files.sum()
    df['file_agg_prob'] = 1.0*df.files_agg/all_files

    valid_ccp_files = vdf.files.sum()
    vdf['vfile_agg_prob'] = 1.0*vdf.valid_files_agg/valid_ccp_files

    print "all files", "{:,}".format(all_files)
    print "valid CCP files", "{:,}".format(valid_ccp_files)
    print "valid files ratio", "{0:2.0f}\%".format(100.0 *valid_ccp_files / all_files)

    vals = [1.0*i/10 for i in range(1, 10)]
    vals.append(0.95)
    vals.append(0.99)


    print "Percentile & Full hit rate & Full CCP & Truncated hit rate & Truncated CCP  \\\\ \hline"
    for i in vals:


        print str(int(100 * i)) + " & " + \
              str(int(100*find_value_index(df, i,  'rhit_rate', 'file_agg_prob'))) + \
              " & " + str(int(100*estimate_ccp(find_value_index(df, i,  'rhit_rate', 'file_agg_prob')))) \
              + " & " + str(int(100*find_value_index(vdf, i,  'rhit_rate', 'vfile_agg_prob'))) \
              + " & " + str(int(100*estimate_ccp(find_value_index(vdf, i,  'rhit_rate', 'vfile_agg_prob')))) + " \\\\ \hline"


    all_hits = df.hits.sum()
    all_commits = df.commits.sum()

    high_ccp = [0.0, 0.9, 0.95, 0.99]
    high_ccp_fixes = {}

    for i in high_ccp:
        high_ccp_fixes[i] = estimate_ccp(1.0 * df[df.rhit_rate > find_value_index(df, i,  'rhit_rate', 'file_agg_prob')].hits.sum()
                     / df[df.rhit_rate > find_value_index(df, i,  'rhit_rate', 'file_agg_prob')].commits.sum()) * \
                df[df.rhit_rate > find_value_index(df, i,  'rhit_rate', 'file_agg_prob')].commits.sum()

    print "focusing in 0.9 file cover bugs", "{0:2.0f}\%".format(100.0 *high_ccp_fixes[0.9] / high_ccp_fixes[0.0])
    print "focusing in 0.99 file cover bugs", "{0:2.0f}\%".format(100.0 *high_ccp_fixes[0.99] / high_ccp_fixes[0.0])

    # write files
    df.to_csv(enhanced_file)
    vdf.to_csv(valid_enhanced_file)

analyse_file_hit_dist('file_hit_rate_dist_atleast_10.csv'
                       , 'file_hit_rate_dist_atleast_10_enhanced.csv'
                      , 'file_hit_rate_dist_atleast_10_valid_enhanced.csv')