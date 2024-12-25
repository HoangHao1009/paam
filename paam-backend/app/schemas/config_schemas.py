from pydantic import BaseModel
from typing import Literal

class ConfigSchema(BaseModel):
    srcPlatform: Literal['questionpro']
    surveyId: str
    apiKey: str
