import os
import requests
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def add_dot_to_readme():
    # Step 1: Add a "." into README.md file
    repo_owner = os.getenv("GITHUB_USERNAME")
    repo_name = os.getenv("REPO_NAME")

    readme_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/README.md"
    response = requests.get(readme_url)

    if response.status_code == 200:
        # Add a dot to the README content
        readme_content = response.text + "."

        # Step 2: Push the change to the GitHub repo
        commit_message = f"Automated commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        update_readme_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/README.md"
        update_readme_payload = {
            "message": commit_message,
            "content": readme_content.encode("base64").decode("utf-8"),  # Base64 encode the new content
            "sha": response.headers["ETag"].replace('"', ''),  # Use the current commit SHA
        }

        github_token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"Bearer {github_token}"}

        update_response = requests.put(update_readme_url, json=update_readme_payload, headers=headers)

        if update_response.status_code == 200:
            print(f"Commit successful: {commit_message}")
        else:
            print(f"Commit failed. Status Code: {update_response.status_code}, Response: {update_response.text}")
    else:
        print(f"Failed to fetch README content. Status Code: {response.status_code}, Response: {response.text}")

# Step 3: Schedule the task to run every day at a specific time
schedule.every().day.at("12:46").do(add_dot_to_readme)  # Adjust the time as needed

while True:
    schedule.run_pending()
    time.sleep(1)
