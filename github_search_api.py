# Import required modules
import requests
import time
import csv

# Paste your Access token here
# To create an access token - https://github.com/settings/tokens
token = "access_token=" + "40291a784587d53f5c271eb1f5c5cc60afb60107"

# Base API Endpoint
base_api_url = 'https://api.github.com/'


# Enter multiple word queries with a '+' sign
# Ex: machine+learning to search for Machine Learning

print('Enter the Search Query to get the Data ')

query = input()
print('\n Query entered is', query, '\n')

search_final_url = base_api_url + 'search/repositories?q=' + query + '&' + token



# A CSV file containting the data would be saved with the name as the query
# Ex: machine+learning.csv
filename = query + '.csv'

# Create a CSV file or clear the existing one with the same name
with open(filename, 'w', newline='') as csvfile:
    write_to_csv = csv.writer(csvfile, delimiter='|')


# GitHub returns information of only 30 repositories with every request
# The Search API Endpoint only allows upto 1000 results, hence the range has been set to 35
for page in range(1, 35):

    # Building the Search API URL
    search_final_url = base_api_url + 'search/repositories?q=' + \
        query + '&page=' + str(page) + '&' + token

    # try-except block just incase you set up the range in the above for loop beyond 35
    try:
        response = requests.get(search_final_url).json()
    except:
        print("Issue with GitHub API, Check your token")

    # Parsing through the response of the search query
    for item in response['items']:
        # Append to the CSV file
        with open(filename, 'a', newline='') as csvfile:
            write_to_csv = csv.writer(csvfile, delimiter='|')

            repo_name = item['name']
            repo_description = item['description']
            repo_stars = item['stargazers_count']
            repo_watchers = item['watchers_count']
            repo_forks = item['forks_count']
            repo_issues_count = item['open_issues_count']
            repo_main_language = item['language']
            repo_license = None
            # repo_score is the relevancy score of a repository to the search query
            # Reference - https://developer.github.com/v3/search/#ranking-search-results
            repo_score = item['score']

            # Many Repositories don't have a license, this is to filter them out
            if item['license']:
                repo_license = item['license']['name']
            else:
                repo_license = "NO LICENSE"

            # Just incase, you face any issue with GitHub API Rate Limiting, use the sleep function as a workaround
            # Reference - https://developer.github.com/v3/search/#rate-limit

            # time.sleep(10)

            # Languages URL to access all the languages present in the repository
            language_url = item['url'] + '/languages?' + token
            language_response = requests.get(language_url).json()

            repo_languages = {}

            # Calculation for the percentage of all the languages present in the repository
            count_value = sum([value for value in language_response.values()])
            for key, value in language_response.items():
                key_value = round((value / count_value) * 100, 2)
                repo_languages[key] = key_value
            print("Repo Name = ", repo_name, "\tDescription", repo_description, "\tStars = ", repo_stars, "\tWatchers = ", repo_watchers, "\tForks = ", repo_forks,
                  "\tOpen Issues = ", repo_issues_count, "\tPrimary Language = ", repo_main_language, "\tRepo Languages =", repo_languages, '\tRepo Score', repo_score)

            # Write as a row to the CSV file
            write_to_csv.writerow([repo_name, repo_description, repo_stars, repo_watchers, repo_forks,
                                   repo_license, repo_issues_count, repo_score, repo_main_language, repo_languages])

            print('==========')