import json
import requests
import numpy as np
import pandas as pd
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth

credentials = json.loads(open('credentials.json').read())  #edit configuration files 
authentication = HTTPBasicAuth(credentials['username'], credentials['password'])
data = requests.get('https://api.github.com/users/' + credentials['username'],
                    auth = authentication)
data = data.json()
#pprint (data)

print("Information about user {}:\n".format(credentials['username']))
print("Name: {}".format(data['name']))
print("Email: {}".format(data['email']))
print("Location: {}".format(data['location']))
print("Public repos: {}".format(data['public_repos']))
print("Public gists: {}".format(data['public_gists']))
print("About: {}".format(data['bio']))

url = data['repos_url']
page_no = 1
repos_data = []
while (True):
    response = requests.get(url, auth = authentication)
    response = response.json()
    repos_data = repos_data + response
    repos_fetched = len(response)
    print("Total repositories fetched: {}".format(repos_fetched))
    if (repos_fetched == 30):
        page_no = page_no + 1
        url = data['repos_url'].encode("UTF-8") + '?page=' + str(page_no)
    else:
        break


repos_information = []
for i, repo in enumerate(repos_data):
    data = []
    data.append(repo['id'])
    data.append(repo['name'])
    data.append(repo['description'])
    data.append(repo['created_at'])
    data.append(repo['updated_at'])
    data.append(repo['owner']['login'])
    data.append(repo['license']['name'] if repo['license'] != None else None)
    data.append(repo['has_wiki'])
    data.append(repo['forks_count'])
    data.append(repo['open_issues_count'])
    data.append(repo['stargazers_count'])
    data.append(repo['watchers_count'])
    data.append(repo['url'])
    data.append(repo['commits_url'].split("{")[0])
    data.append(repo['url'] + '/languages')
    repos_information.append(data)
repos_df = pd.DataFrame(repos_information, columns = ['Id', 'Name', 'Description', 'Created on', 'Updated on', 
                                                      'Owner', 'License', 'Includes wiki', 'Forks count', 
                                                      'Issues count', 'Stars count', 'Watchers count',
                                                      'Repo URL', 'Commits URL', 'Languages URL'])

#print ("\n\n.\n.\n",repos_df)
#for i in range(repos_df.shape[0]):
#    response = requests.get(repos_df.loc[i, 'Languages URL'], auth = authentication)
#    response = response.json()
#    print(i, response)
#    if response != {}:
#        languages = []
#        for key, value in response.items():
#            languages.append(key)
#        languages = ', '.join(languages)
#        repos_df.loc[i, 'Languages'] = languages
#    else:
#        repos_df.loc[i, 'Languages'] = ""

commits_information = []
for i in range(repos_df.shape[0]):
    url = repos_df.loc[i, 'Commits URL']
    page_no = 1
    while (True):
        response = requests.get(url, auth = authentication)
        response = response.json()
        print("URL: {}, commits: {}".format(url, len(response)))
        for commit in response:
            commit_data = []
            commit_data.append(repos_df.loc[i, 'Id'])
            commit_data.append(commit['sha'])
            commit_data.append(commit['commit']['committer']['date'])
            commit_data.append(commit['commit']['message'])
            commits_information.append(commit_data)
        if (len(response) == 30):
            page_no = page_no + 1
            url = repos_df.loc[i, 'Commits URL'] + '?page=' + str(page_no)
        else:
            break
            
commits_df = pd.DataFrame(commits_information, columns = ['Repo Id', 'Commit Id', 'Date', 'Message'])
commits_df.to_csv('commits_info.csv', index = False)

