import requests
import os

def get_github_token():
    # Retrieve the GitHub token from environment variables or a configuration file
    return os.getenv('GITHUB_TOKEN')

def create_github_issue(repo_owner, repo_name, title, body):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    headers = {
        'Authorization': f'token {get_github_token()}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': title,
        'body': body
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def main():
    repo_owner = 'msuatgunerli'
    repo_name = 'refurb-tracker'
    title = 'Nikon Refurb Alert'
    body = 'Refurbished deals found.'

    try:
        issue = create_github_issue(repo_owner, repo_name, title, body)
        if 'number' in issue:
            issue_id = issue['number']
            print(f'Issue created with ID: {issue_id}')
        else:
            print('Issue created, but ID not found in response.')
    except requests.exceptions.HTTPError as e:
        print(f'GitHub API request failed: {e}')
    except KeyError as e:
        print(f'KeyError: {e}')

if __name__ == '__main__':
    main()