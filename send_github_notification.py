import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import requests

GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')
GITHUB_API_URL = "https://api.github.com/repos/msuatgunerli/refurb-tracker/issues"
ISSUE_TITLE = "Nikon Scraper Results"

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

def comment_on_issue(issue_id, comment):
    url = f"https://api.github.com/repos/msuatgunerli/refurb-tracker/issues/{issue_id}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": comment
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def main():
    issue_id = get_issue_id()
    if issue_id is None:
        issue = create_issue()
        issue_id = issue['number']

    results = format_results()
    comment_on_issue(issue_id, results)

    # Send email notification
    subject = "Nikon Scraper Results"
    body = results
    to_email = os.getenv('TO_EMAIL')
    send_email(subject, body, to_email)

if __name__ == "__main__":
    main()