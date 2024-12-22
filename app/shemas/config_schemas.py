from pydantic import BaseModel
from typing import Literal

class ConfigSchema(BaseModel):
    src_platform: Literal['questionpro']
    survey_id: str
    api_key: str
