from pydantic import BaseModel
from typing import Literal, List

class ConfigSchema(BaseModel):
    srcPlatform: Literal['questionpro']
    surveyId: str
    apiKey: str
    
class CreateSchema(BaseModel):
    surveyId: str