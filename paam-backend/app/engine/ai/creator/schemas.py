from pydantic import BaseModel, Field
from typing import List, Optional

class Answer(BaseModel):
    """Information about an answer option in a question."""
    text: str = Field(..., description="The text of the answer option, e.g., '16 years old'.")

class Question(BaseModel):
    """Information about a question in the survey or questionnaire."""
    code: str = Field(..., description="Unique identifier for the question, e.g., 'Q1', 'S1.2'.")
    type: str = Field(..., description="Type of the question: 'sa' for single answer, 'ma' for multiple answers, 'oe' for open-ended.")
    text: str = Field(..., description="The actual content of the question, e.g., 'How old are you?'.")
    answers: List[Answer] = Field(..., description="List of possible answer options to the question.")

class Info(BaseModel):
    """A collection of questions with answers to be extracted."""
    questions: List[Question] = Field(..., description="A list of questions with their answer options.")
