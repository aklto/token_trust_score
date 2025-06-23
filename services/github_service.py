from github import Github
from config import GITHUB_TOKEN

g = Github(GITHUB_TOKEN)

def get_repo_data(repo_full_name: str):
    repo = g.get_repo(repo_full_name)
    try:
        readme = repo.get_readme().decoded_content.decode('utf-8')
    except:
        readme = ""
    return {
        'description': repo.description or "",
        'readme': readme,
        'stars': repo.stargazers_count,
        'forks': repo.forks_count,
        'created_at': repo.created_at,
        'open_issues': repo.open_issues_count,
        'repo': repo
    }
