# checks/check_docs.py
from github import Github
import os, sys

def docs_ok(repo_full_name, pr_number, gh_token):
    gh = Github(gh_token)
    repo = gh.get_repo(repo_full_name)
    pr = repo.get_pull(int(pr_number))
    files = [f.filename for f in pr.get_files()]
    for f in files:
        if f.lower().startswith("changelog") or f.lower().startswith("docs/") or f.lower() == "readme.md":
            return True
    return False

if __name__ == "__main__":
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr = os.environ.get("PR_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")
    if not repo or not pr or not token:
        print("Missing env variables")
        sys.exit(2)
    ok = docs_ok(repo, pr, token)
    print("Docs OK" if ok else "Docs MISSING")
    sys.exit(0 if ok else 1)
