import requests
import os
from datetime import datetime

def get_ci_cycle_time():
    """
    Fetch the latest workflow run for 'CI Pipeline' and calculate the duration.
    This demonstrates DORA metrics monitoring for Cycle Time.
    """
    # GitHub repository details
    owner = "4tis430"
    repo = "gear-tracker-api"
    workflow_name = "CI Pipeline"
    
    # GitHub API endpoint for workflow runs
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    
    # Optional: Use GitHub token for higher rate limits
    headers = {}
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        # Fetch workflow runs
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        workflow_runs = data.get("workflow_runs", [])
        
        if not workflow_runs:
            print("No workflow runs found.")
            return
        
        # Get the latest completed workflow run
        latest_run = None
        for run in workflow_runs:
            if run.get("name") == workflow_name and run.get("status") == "completed":
                latest_run = run
                break
        
        if not latest_run:
            print(f"No completed runs found for workflow '{workflow_name}'.")
            return
        
        # Calculate duration
        created_at = datetime.strptime(latest_run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        updated_at = datetime.strptime(latest_run["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        duration_seconds = int((updated_at - created_at).total_seconds())
        
        # Print DORA metric
        print(f"Current Cycle Time (CI): {duration_seconds} seconds")
        
        # Additional info
        print(f"Workflow: {latest_run['name']}")
        print(f"Status: {latest_run['conclusion']}")
        print(f"Run ID: {latest_run['id']}")
        print(f"URL: {latest_run['html_url']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching workflow data: {e}")
    except Exception as e:
        print(f"Error processing workflow data: {e}")

if __name__ == "__main__":
    get_ci_cycle_time()
