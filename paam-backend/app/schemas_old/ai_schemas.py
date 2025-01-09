from pydantic import BaseModel
from typing import List

class ChatSchema(BaseModel):
    message: str
    
class CreateSchema(BaseModel):
    surveyId: str