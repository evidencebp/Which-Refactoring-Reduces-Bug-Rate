"""
The following script extrat repositories properties from the GitHub API.

In order to use the script one should deploy the gitHub python client from
https://github.com/PyGithub/PyGithub

Other than than one should create a user in the Github site and supply
the credentials.

Git limits the number of requests to 5,000 per hour.
Note that querying each property is a request so one should remove
unneeded properties.

The fork property is of special interest since that due to the forking
the GitHub BigQuery database contain plenty redundent repositories.
Filtering out forks can take care of that.

"""

from github import Github
import pandas
import requests
from time import sleep



git_interface = Github('user', 'password')



def extract_projects_properties_quota(projects_list
                                     , properties_file
                                     , git_interface):
    """
        Extract repositories properties and mange quota.
        Calling this function enable runing the script over night.


    :param projects_list:
    :param properties_file:
    :param git_interface:
    :return:
    """

    # Git quota is 5000 but we do 8 calls
    BATCH = 100
    CALLS = 8
    all_df = None

    for i in range(len(projects_list) /QUOTA_BATCH):

     no_quota = True
     while no_quota:
         try:
             if git_interface.get_rate_limit() > CALLS*BATCH:
                 no_quota = False
         except requests.exceptions.SSLError:
             print "sleeping"
             sleep(60)

     print "processing batch " + str(i)
     df = extract_projects_properties(projects_list[i: i+BATCH]
                                    , properties_file
                                    , git_interface)
     all_df = pandas.concat([all_df, df])
     all_df.to_csv(properties_file + "_" +str(i))


    all_df.to_csv(properties_file + "all")

    return all_df

def extract_projects_properties(projects_list
                                    , properties_file
                                    , git_interface):
    """
        Extract reopsitories properties
    :param projects_list:
    :param properties_file:
    :param git_interface:
    :return:
    """

    BATCH_SIZE = 10

    properties_list = []
    current_item = 0

    for project in projects_list:
        current_item += 1
        if current_item % BATCH_SIZE == 0:
            print "proccesing item # " + str(current_item)
        try:
            repo = git_interface.get_repo(project)
            properties_dict  =  extract_repo_properties(repo)
            properties_dict['name'] = project
            properties_list.append(properties_dict)

        except:
            print "error parsing " + project

    df = pandas.DataFrame(properties_list)

    df.to_csv(properties_file)



    return df



def extract_repo_properties(repo):
    """
    Extract repository properties.

    Note that a repository's propeties might not be found due to
    few cases:
    - Reporitory was deleted
    - Repository was renamed
    - Repository was turn private
    - Qouta was used
    - A temporal error in the API

    Due to the last two reseaon it is recommended to run the script more
    than once.

    :param repo:
    :return:
    """
    properties = {}

    try:
        properties['contributors_count'] = len([ i for i in repo.get_contributors()])
    except:
        print "error reading contributors list"
        
    properties['forks_count'] = repo.forks_count
    properties['language'] = repo.language
    properties['network_count'] = repo.network_count
    properties['open_issues_count']  = repo.open_issues_count
    properties['stargazers_count']  = repo.stargazers_count
    properties['subscribers_count'] = repo.subscribers_count
    properties['watchers_count'] = repo.watchers_count
    properties['fork'] = repo.fork


    return properties

