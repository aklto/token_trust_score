from pydantic import BaseModel

class TokenRequest(BaseModel):
    token_id: str
    github_repo: str
    contract_address: str
