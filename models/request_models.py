from pydantic import BaseModel
from typing import Optional

class TokenRequest(BaseModel):
    token_id: str
    contract_address: str
    github_repo: Optional[str] = None
