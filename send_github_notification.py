# import os
# import json
# import requests
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # GitHub settings
# GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
# REPO_OWNER = "msuatgunerli"  # GitHub username or organization
# REPO_NAME = "refurb-tracker"  # GitHub repository name
# ISSUE_TITLE = "Nikon Scraper Results"  # The issue title

# # GitHub API URL
# GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

# # Function to check if the issue already exists
# def get_issue_id():
#     headers = {
#         "Authorization": f"Bearer {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     response = requests.get(GITHUB_API_URL, headers=headers)

#     try:
#         response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
#         issues = response.json()

#         # Make sure it's a list
#         if not isinstance(issues, list):
#             print("Unexpected issues response:", issues)
#             return None

#         for issue in issues:
#             print(issue)
#             if issue.get('title') == ISSUE_TITLE:
#                 return issue['number']
#         return None

#     except requests.exceptions.RequestException as e:
#         print("GitHub API request failed:", e)
#         print("Response content:", response.text)
#         return None

# # Function to create a new issue
# def create_issue():
#     headers = {
#         "Authorization": f"Bearer {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     data = {
#         "title": ISSUE_TITLE,
#         "body": "Nikon scraper results will appear here."
#     }
#     response = requests.post(GITHUB_API_URL, headers=headers, json=data)
#     return response.json()

# # Function to comment on an existing issue
# def comment_on_issue(issue_id, comment):
#     url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_id}/comments"
#     headers = {
#         "Authorization": f"Bearer {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     data = {
#         "body": comment
#     }
#     response = requests.post(url, headers=headers, json=data)
#     return response.json()

# # Function to format the log data into a message
# def format_results():
#     with open("product_status_log.json", "r") as f:
#         data = json.load(f)

#     result_message = "### Nikon Scraper Results\n\n"
#     for item in data:
#         result_message += f"- **URL**: {item['url']}\n"
#         result_message += f"  - **Stock Status**: {item['stock_status']}\n"
#         if item['stock_status'] == "In Stock":
#             result_message += f"  - **Sale Price**: ${item['sale_price']}\n"
#             result_message += f"  - **Original Price**: ${item['original_price']}\n"
#             result_message += f"  - **You Save**: ${item['you_save']}\n"
#             result_message += f"  - **Discount Label**: {item['discount_label']}\n"
#             result_message += f"  - **Discount Percentage**: {item['calculated_discount_pct']}%\n"
#         result_message += "\n"

#     return result_message

# # Function to send an email
# def send_email(subject, body, to_email):
#     from_email = os.getenv('FROM_EMAIL')
#     from_password = os.getenv('FROM_PASSWORD')
#     smtp_server = os.getenv('SMTP_SERVER')
#     smtp_port = os.getenv('SMTP_PORT')

#     print(f"Sending email from {from_email} to {to_email} via {smtp_server}:{smtp_port}")

#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(from_email, from_password)
#         text = msg.as_string()
#         server.sendmail(from_email, to_email, text)
#         server.quit()
#         print("Email sent successfully")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# # Main function to execute the script
# def main():
#     issue_id = get_issue_id()
#     if issue_id is None:
#         issue = create_issue()
#         issue_id = issue['number']

#     results = format_results()
#     comment_on_issue(issue_id, results)

#     # Send email notification
#     subject = "Nikon Scraper Results"
#     body = results
#     to_email = os.getenv('TO_EMAIL')
#     send_email(subject, body, to_email)

# if __name__ == "__main__":
#     main()

import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    in_stock_items = []

    for item in data:
        result_message += f"- **URL**: {item['url']}\n"
        result_message += f"  - **Stock Status**: {item['stock_status']}\n"
        if item['stock_status'] == "In Stock":
            result_message += f"  - **Sale Price**: ${item['sale_price']}\n"
            result_message += f"  - **Original Price**: ${item['original_price']}\n"
            result_message += f"  - **You Save**: ${item['you_save']}\n"
            result_message += f"  - **Discount Label**: {item['discount_label']}\n"
            result_message += f"  - **Discount Percentage**: {item['calculated_discount_pct']}%\n"
            in_stock_items.append(item)
        result_message += "\n"

    return result_message, in_stock_items

# Function to send an email
def send_email(subject, body, to_email):
    from_email = os.getenv('FROM_EMAIL')
    from_password = os.getenv('FROM_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')

    print(f"Sending email from {from_email} to {to_email} via {smtp_server}:{smtp_port}")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function to execute the script
def main():
    issue_id = get_issue_id()
    if issue_id is None:
        issue = create_issue()
        issue_id = issue['number']

    results, in_stock_items = format_results()
    comment_on_issue(issue_id, results)

    # Send email notification only if there are in-stock items
    if in_stock_items:
        subject = "Nikon Scraper Results"
        body = results
        to_email = os.getenv('TO_EMAIL')
        send_email(subject, body, to_email)

if __name__ == "__main__":
    main()