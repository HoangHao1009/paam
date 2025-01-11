from pydantic import BaseModel
from typing import Literal

class QuestionComputeSchema(BaseModel):
    method: Literal["classify", "cluster"]
    rootQuestionCode: str
    newQuestionCode: str
    newQuestionText: str
    construction: str
    by: Literal["text", "scale"]

class DeleteConstructionSchema(BaseModel):
    questionCode: str