import pandas as pd


def estimate_ccp(hr):
    return 1.193*hr - 0.06

def build_repos(bigquery_repo_file
                , gitapi_repo_file
                , full_repo_file
                , valid_repo_file):

    repos = pd.read_csv(bigquery_repo_file)
    repos_api = pd.read_csv(gitapi_repo_file)

    repos_api = repos_api.rename(columns={'name' : 'repo_name'})
    repos_full = pd.merge(repos, repos_api, on='repo_name')

    repos_full['y2016_hit_rate'] = 1.0*repos_full.y2016_hits/repos_full.y2016_commits
    repos_full['y2016_ccp'] = repos_full.y2016_hit_rate.map(lambda x: estimate_ccp(x))
    repos_full['y2017_hit_rate'] = 1.0*repos_full.y2017_hits/repos_full.y2017_commits
    repos_full['y2017_ccp'] = repos_full.y2017_hit_rate.map(lambda x: estimate_ccp(x))
    repos_full['y2018_hit_rate'] = 1.0*repos_full.y2018_hits/repos_full.y2018_commits
    repos_full['y2018_ccp'] = repos_full.y2018_hit_rate.map(lambda x: estimate_ccp(x))
    repos_full = repos_full.rename(columns={'hit_ratio' : 'hit_rate'})

    repos_full.to_csv(full_repo_file, index=False)
    valid_repos = repos_full[(repos_full.fork ==False) &(repos_full.y2018_ccp >0) & (repos_full.y2018_ccp <1)]
    valid_repos.to_csv(valid_repo_file, index=False)

    print "number of 2018 reopsitories", "{:,}".format(len(repos))
    print "number of 2018 reopsitories found in api", "{:,}".format(len(repos_api)), "{0:2.0f}\%".format(100.0*len(repos_api)/len(repos))
    print "number of 2018 reopsitories found in api that are not forks", "{:,}".format(
        len(repos_full[repos_full.fork ==False])), "{0:2.0f}\%".format(
        100.0*len(repos_full[repos_full.fork ==False])/len(repos_full))
    print "number of 2018 valid reopsitories", "{:,}".format(
        len(valid_repos)), "{0:2.0f}\%".format(100.0*len(valid_repos)/len(repos_full[repos_full.fork ==False]))
    print "valid C repositories", "{:,}".format(len(valid_repos[valid_repos.language == 'C']))


build_repos('repos2018.csv'
                , 'repos2018_api.csv'
                , 'repos_full.csv'
                , 'valid_repos.csv')