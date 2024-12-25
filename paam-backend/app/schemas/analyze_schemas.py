from pydantic import BaseModel
from typing import List

class CrossTabSchema(BaseModel):
    base: str
    target: str
    deepBy: List[str]