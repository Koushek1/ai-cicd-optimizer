import requests
import os
import psycopg2
from datetime import datetime

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "yourusername/ai-cicd-optimizer"  # Replace with your actual repo

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

DB = psycopg2.connect(
    dbname="ci_data", user="postgres", password="yourpassword", host="localhost", port="5432"
)
CURSOR = DB.cursor()

def store_run(run):
    CURSOR.execute(
        """
        INSERT INTO builds (run_id, status, duration_minutes, commit_hash, author, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            run["id"],
            run["conclusion"],
            (datetime.fromisoformat(run["updated_at"][:-1]) - datetime.fromisoformat(run["created_at"][:-1])).total_seconds() / 60.0,
            run["head_sha"],
            run["head_commit"]["author"]["name"],
            run["created_at"]
        )
    )
    DB.commit()

def get_runs():
    url = f"https://api.github.com/repos/{REPO}/actions/runs"
    res = requests.get(url, headers=headers)
    runs = res.json().get("workflow_runs", [])
    for run in runs:
        store_run(run)
    print(f"Stored {len(runs)} runs.")

get_runs()
