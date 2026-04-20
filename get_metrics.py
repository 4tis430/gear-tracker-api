import requests
import os
from datetime import datetime

def get_dora_metrics():
    """
    Calculate DORA metrics by tracking the complete pipeline:
    - Commit time (from GitHub)
    - CI completion time (GitHub Actions)
    - Deployment time (Render startup)
    """
    # GitHub repository details
    owner = "4tis430"
    repo = "gear-tracker-api"
    workflow_name = "CI Pipeline"
    
    # Optional: Use GitHub token for higher rate limits
    headers = {}
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        # Step 1: Get the latest commit time from main branch
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits/main"
        commits_response = requests.get(commits_url, headers=headers)
        commits_response.raise_for_status()
        
        commit_data = commits_response.json()
        commit_time_str = commit_data["commit"]["committer"]["date"]
        commit_time = datetime.strptime(commit_time_str, "%Y-%m-%dT%H:%M:%SZ")
        
        print("=" * 60)
        print("DORA METRICS - Lead Time for Changes")
        print("=" * 60)
        print(f"\n📝 Latest Commit: {commit_data['sha'][:7]}")
        print(f"   Message: {commit_data['commit']['message'].split(chr(10))[0]}")
        print(f"   Time: {commit_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Step 2: Get the latest workflow run for CI time
        workflow_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
        workflow_response = requests.get(workflow_url, headers=headers)
        workflow_response.raise_for_status()
        
        workflow_data = workflow_response.json()
        workflow_runs = workflow_data.get("workflow_runs", [])
        
        latest_run = None
        for run in workflow_runs:
            if run.get("name") == workflow_name and run.get("status") == "completed":
                latest_run = run
                break
        
        if not latest_run:
            print(f"\n⚠️  No completed workflow runs found for '{workflow_name}'")
            return
        
        ci_start = datetime.strptime(latest_run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        ci_end = datetime.strptime(latest_run["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        ci_duration = int((ci_end - ci_start).total_seconds())
        
        print(f"\n⚙️  CI Pipeline (GitHub Actions)")
        print(f"   Status: {latest_run['conclusion']}")
        print(f"   Duration: {ci_duration} seconds")
        print(f"   Completed: {ci_end.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Step 3: Get deployment timestamp from Render
        api_url = "https://gear-tracker-api.onrender.com/guitars"
        api_response = requests.get(api_url, timeout=10)
        api_response.raise_for_status()
        
        api_data = api_response.json()
        deployment_timestamp_str = api_data.get("deployment_timestamp")
        
        if not deployment_timestamp_str:
            print("\n⚠️  No deployment_timestamp found in API response")
            return
        
        # Parse ISO format timestamp (may include microseconds and timezone)
        if "." in deployment_timestamp_str:
            # Has microseconds
            deployment_time = datetime.fromisoformat(deployment_timestamp_str.replace("Z", "+00:00"))
        else:
            deployment_time = datetime.fromisoformat(deployment_timestamp_str.replace("Z", "+00:00"))
        
        # Convert to UTC naive datetime for comparison
        deployment_time = deployment_time.replace(tzinfo=None)
        
        print(f"\n🚀 Deployment (Render)")
        print(f"   Startup Time: {deployment_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Step 4: Calculate metrics
        cd_duration = int((deployment_time - ci_end).total_seconds())
        total_lead_time = int((deployment_time - commit_time).total_seconds())
        
        print("\n" + "=" * 60)
        print("📊 METRICS BREAKDOWN")
        print("=" * 60)
        print(f"⏱️  CI Time (GitHub Actions):     {ci_duration} seconds ({ci_duration // 60}m {ci_duration % 60}s)")
        print(f"⏱️  CD Time (Render Deployment):  {cd_duration} seconds ({cd_duration // 60}m {cd_duration % 60}s)")
        print(f"⏱️  Total Lead Time:              {total_lead_time} seconds ({total_lead_time // 60}m {total_lead_time % 60}s)")
        print("=" * 60)
        
        # DORA classification
        if total_lead_time < 3600:  # Less than 1 hour
            classification = "🌟 Elite"
        elif total_lead_time < 86400:  # Less than 1 day
            classification = "🚀 High"
        elif total_lead_time < 604800:  # Less than 1 week
            classification = "📈 Medium"
        else:
            classification = "📉 Low"
        
        print(f"\n🎯 DORA Performance: {classification}")
        print("=" * 60)
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching data: {e}")
    except Exception as e:
        print(f"\n❌ Error processing data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_dora_metrics()
