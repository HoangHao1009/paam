import pandas as pd
from .core_question import Question
from .answer import Answer
from .helper_function import _get_duplicates
from ..utils import spss_function
from typing import List

class Number(Question):
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer]):
        super().__init__(id, code, text, order, type, answers)
        self.respondents = self._get_respondents()
    
    def _get_respondents(self):
        respondents = []
        for answers in self.answers:
            respondents.extend(answers.respondents)
        invalid = _get_duplicates(respondents)
        
        if len(respondents) == 0:
            raise AttributeError(f"Question have no respondent")
        
        if len(invalid) > 0:
            raise ValueError(f"Error - Duplicates occurs: {invalid}")
        
        return respondents
        
    @property
    def spss_syntax(self):
        code = self.code
        to_scale = f'VARIABLE LEVEL {code} (SCALE).'
        return [spss_function.var_label(code, self.text), to_scale]
    
    @property
    def df(self):
        data = [
            {'R_ID': respondent, self.code: int(answer.text)}
            for answer in self.answers 
            for respondent in answer.respondents
        ]
        
        df = pd.DataFrame(data)
        
        if self._ctab_mode:
            return df
        else:
            return df.set_index('R_ID')
    
