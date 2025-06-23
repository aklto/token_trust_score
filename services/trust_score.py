from datetime import datetime, timezone, timedelta
from utils.normalization import normalize

def calculate_trust_score(token_data, repo_data, contract_data, embedding):
    now = datetime.now(timezone.utc)

    market_cap_score = normalize(token_data['market_cap'], 1e6, 1e11)
    volume_score = normalize(token_data['volume'], 1e4, 1e10)
    liquidity_score = normalize(token_data['volume'] / token_data['market_cap'], 0.01, 0.5)
    age_score = normalize(token_data['age_days'], 0, 4000)

    repo_age_days = (now - repo_data['created_at']).days
    repo_age_score = normalize(repo_age_days, 0, 4000)
    stars_score = normalize(repo_data['stars'], 0, 50000)
    forks_score = normalize(repo_data['forks'], 0, 20000)

    try:
        commits = repo_data['repo'].get_commits(since=now - timedelta(days=90)).totalCount
    except:
        commits = 0
    commit_score = normalize(commits, 0, 500)
    is_org_score = 1.0 if repo_data['repo'].owner.type == "Organization" else 0.5
    try:
        closed_issues = repo_data['repo'].get_issues(state='closed').totalCount
        open_issues = repo_data['open_issues']
        issue_score = closed_issues / (closed_issues + open_issues) if (closed_issues + open_issues) > 0 else 0.5
    except:
        issue_score = 0.5

    verified_score = 1.0 if contract_data['is_verified'] else 0.3
    holders_score = normalize(contract_data['holders_count'], 100, 50000)
    top_holder_score = 1.0 - normalize(contract_data['top_holder_ratio'], 0, 1)
    dangerous_score = 0.0
    if contract_data['has_delegatecall']:
        dangerous_score -= 0.3
    if contract_data['has_selfdestruct']:
        dangerous_score -= 0.2

    total_score = (
        0.15 * market_cap_score +
        0.1 * volume_score +
        0.1 * liquidity_score +
        0.05 * age_score +
        0.05 * repo_age_score +
        0.1 * stars_score +
        0.05 * forks_score +
        0.1 * commit_score +
        0.05 * is_org_score +
        0.05 * issue_score +
        0.05 * verified_score +
        0.05 * holders_score +
        0.05 * top_holder_score +
        0.05 * dangerous_score
    )
    return max(min(total_score, 1.0), 0.0)
