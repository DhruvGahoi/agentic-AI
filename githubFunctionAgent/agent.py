import os
import sys
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Create Repository Tool

def github_create_repo_tool(repo_name: str, description: str = "", private: bool = True):
    """Creates a new GitHub repository."""

    if not GITHUB_TOKEN:
        print("Error: GitHub token not found in environment.", file=sys.stderr)
        return

    api_url = "https://api.github.com/user/repos" 

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": False
    }

    print(f"Attempting to create GitHub repository: {repo_name}")

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()

        repo_data = response.json()
        print(f"Successfully created GitHub repository: {repo_data['html_url']}")
        print("Use the following commands to link your local repository:")
        print(f"  git remote add origin {repo_data['clone_url']}")
        print(f"  git push -u origin main")

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 422:
            print(f"Error: A repository with the name '{repo_name}' already exists.", file=sys.stderr)
        else:
            print(f"HTTP Error: {err}", file=sys.stderr)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)


# Delete Repository Tool

def github_delete_repo_tool(repo_name: str):
    """Deletes a GitHub repository."""

    if not GITHUB_USERNAME:
        print("Error: GitHub username missing.", file=sys.stderr)
        return

    if not GITHUB_TOKEN:
        print("Error: GitHub token missing.", file=sys.stderr)
        return

    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"Attempting to delete GitHub repository: {repo_name}")

    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 204:
            print(f"Successfully deleted GitHub repository: {repo_name}")

    except requests.exceptions.HTTPError as err:
        status = err.response.status_code
        if status == 404:
            print(f"Error: Repository '{repo_name}' not found.", file=sys.stderr)
        elif status == 403:
            print("Error: Forbidden — token may lack 'delete_repo' permission.", file=sys.stderr)
        else:
            print(f"HTTP Error: {err}", file=sys.stderr)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)


# Root Agent

from google.adk.agents import Agent

root_agent = Agent(
    name="github_repo_agent",
    model="gemini-2.5-flash",
    description="Agent that creates & deletes GitHub repositories.",
    instruction="""
        If user wants to create a repository:
            - Ask repo name, description, private/public.
        If user wants to delete a repository:
            - Ask repo name.
        Always confirm before deleting a repository since it is irreversible.
    """,
    tools=[github_create_repo_tool, github_delete_repo_tool]
)
