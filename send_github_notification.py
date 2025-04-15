import os
import json
import requests

# GitHub settings
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
REPO_OWNER = "msuatgunerli"  # GitHub username or organization
REPO_NAME = "refurb-tracker"  # GitHub repository name
ISSUE_TITLE = "Nikon Scraper Results"  # The issue title

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

# Function to check if the issue already exists
def get_issue_id():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(GITHUB_API_URL, headers=headers)

    try:
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        issues = response.json()

        # Make sure it's a list
        if not isinstance(issues, list):
            print("Unexpected issues response:", issues)
            return None

        for issue in issues:
            print(issue)
            if issue.get('title') == ISSUE_TITLE:
                return issue['number']
        return None

    except requests.exceptions.RequestException as e:
        print("GitHub API request failed:", e)
        print("Response content:", response.text)
        return None

# Function to create a new issue
def create_issue():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": ISSUE_TITLE,
        "body": "Nikon scraper results will appear here."
    }
    response = requests.post(GITHUB_API_URL, headers=headers, json=data)
    return response.json()

# Function to comment on an existing issue
def comment_on_issue(issue_id, comment):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_id}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": comment
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to format the log data into a message
def format_results():
    with open("product_status_log.json", "r") as f:
        data = json.load(f)
    
    result_message = "### Nikon Scraper Results\n\n"
    for item in data:
        result_message += f"- **URL**: {item['url']}\n"
        result_message += f"  - **Stock Status**: {item['stock_status']}\n"
        if item['stock_status'] == "In Stock":
            result_message += f"  - **Sale Price**: ${item['sale_price']}\n"
            result_message += f"  - **Original Price**: ${item['original_price']}\n"
            result_message += f"  - **You Save**: ${item['you_save']}\n"
            result_message += f"  - **Discount Label**: {item['discount_label']}\n"
            result_message += f"  - **Discount Percentage**: {item['calculated_discount_pct']}%\n"
        result_message += "\n"

    return result_message

def main():
    issue_id = get_issue_id()
    if issue_id is None:
        issue = create_issue()
        issue_id = issue['number']
    
    results = format_results()
    comment_on_issue(issue_id, results)

if __name__ == "__main__":
    main()