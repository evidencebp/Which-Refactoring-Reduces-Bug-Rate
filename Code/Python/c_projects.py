import pandas as pd



valid = pd.read_csv('valid_repos.csv')
ext = pd.read_csv('repos2018_major_extensions.csv')
exclude = pd.read_csv('repo_exclusion.csv')
df = pd.merge(valid, ext, on='repo_name')
df = pd.merge(df, exclude, on='repo_name', how='left')

# 20 files is the 10th precentile
print df[(df.files > 20) & ((df.major_extension == '.c')
         | (df.language == 'C'))].groupby(['major_extension', 'language']).agg({'repo_name' :'count'})

print "major but not by git"
print df[(df.files > 20) &((df.major_extension == '.c') & (df.language != 'C'))][
    ['repo_name', 'major_extension', 'language', 'files', 'major_extension_ratio']]

print "C by git but not major"
print df[(df.files > 20) & ((df.major_extension != '.c') & (df.language == 'C'))][
    ['repo_name', 'major_extension', 'language', 'files', 'major_extension_ratio']]

c_repos = df[(df.files > 20) & ((df.major_extension == '.c')
                      & (df.exclude_from_c != True ))]


c_repos['last_name'] = c_repos.repo_name.map(lambda x: x.split("/")[1])
g = c_repos.groupby(['last_name'], as_index=False).agg({'repo_name' :'count'})
print "simlar last name - examine"
print g[g.repo_name>1]

c_repos.to_csv('c_repos.csv', index=False)