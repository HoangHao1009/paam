from pydantic import BaseModel
from typing import List

class CrossTabSchema(BaseModel):
    base: str
    target: str
    deepBy: List[str]
    alpha: float = 0,
    pct: bool = False,
    round_digit: int = 0,
