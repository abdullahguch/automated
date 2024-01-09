import os
import requests
import schedule
import time
import base64
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def add_dot_to_readme():
    # Step 1: Add a "." into README.md file
    repo_owner = os.getenv("GITHUB_USERNAME")
    repo_name = os.getenv("REPO_NAME")

    readme_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/updated_file.txt"
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(readme_url, headers=headers)

    if response.status_code == 200:
        readme_content = base64.b64decode(response.json()["content"]).decode("utf-8")
        updated_content = readme_content + "."

        # Base64 encode the updated content
        updated_content_base64 = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

        # Step 2: Push the change to the GitHub repo
        commit_message = f"Automated commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        update_readme_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/updated_file.txt"
        update_readme_payload = {
            "message": commit_message,
            "content": updated_content_base64,
            "sha": response.json()["sha"],
        }

        update_response = requests.put(update_readme_url, json=update_readme_payload, headers=headers)

        if update_response.status_code == 200:
            print(f"Commit successful: {commit_message}")
        else:
            print(f"Commit failed. Status Code: {update_response.status_code}, Response: {update_response.text}")
    else:
        print(f"Failed to fetch README content. Status Code: {response.status_code}, Response: {response.text}")

# Step 3: Schedule the task to run every day at a specific time
schedule.every().day.at("01:11").do(add_dot_to_readme)  # Adjust the time as needed

while True:
    schedule.run_pending()
    time.sleep(1)
