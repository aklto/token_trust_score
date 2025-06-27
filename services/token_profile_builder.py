
def build_token_profile(meta: dict, tx_count: int, recent_mints: int, recent_burns: int) -> str:
    age_days = meta.get("age_days", "unknown")
    return f"""
Token Name: {meta.get('name')}
Symbol: {meta.get('symbol')}
Verified: {meta.get('verified')}
Created: {meta.get('created_at')} ({age_days} days ago)
Holders: {meta.get('holders_count')}
Top Holder Owns: {meta.get('top_holder_ratio', 0) * 100:.1f}%
Mint Authority Present: {meta.get('mint_authority') is not None}
Freeze Authority Present: {meta.get('freeze_authority') is not None}
Total Transactions (30d): {tx_count}
Recent Mint Events: {recent_mints}
Recent Burn Events: {recent_burns}
""".strip()
