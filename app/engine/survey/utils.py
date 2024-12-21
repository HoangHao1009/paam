import pandas as pd
from io import BytesIO
from typing import List, Union
from ..question import Single, Multiple, Number, Rank, Answer

question_type = Union[Single, Multiple, Number, Rank]    

def _check_elements(list_check: List[str], questions: List[question_type]):
    question_codes = [question.code for question in questions]
    for question in list_check:
        if question not in question_codes:
            raise KeyError(f"Question {question} not exist in survey")

def _to_excel_buffer(df: pd.DataFrame, sheet_name: str) -> BytesIO:
    """Helper function to write a DataFrame to an Excel buffer."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True, sheet_name=sheet_name)
    output.seek(0)
    return output

