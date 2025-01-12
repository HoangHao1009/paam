from typing import List
import pandas as pd

from .core_question import Question
from .answer import Answer
from .helper_function import _get_duplicates
from ..utils import spss_function
from .number import Number

class Single(Question):
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer]):
        super().__init__(id, code, text, order, type, answers)
        self.respondents = self._get_respondents()
        self.scale_encode: bool = False

    def _get_respondents(self):
        respondents = []
        for answers in self.answers:
            respondents.extend(answers.respondents)
            
        if len(respondents) == 0:
            raise AttributeError(f"Question {self.code} have no respondent")
            
        invalid = _get_duplicates(respondents)
        
        if len(invalid) > 0:
            raise ValueError(f"Error - Duplicates occurs: {invalid}")
        
        return respondents
    
    @property
    def spss_syntax(self):
        code = self.code
        value_label_dict = {index: answers.text for index, answers in enumerate(self.answers, 1)}
        var_label_command = spss_function.var_label(code, self.text)
        value_label_command = spss_function.value_label(code, value_label_dict)
        return [var_label_command, value_label_command]
    
    def to_number(self) -> Number:
        return Number(**self.__dict__)
    
    @property
    def df(self):
        data = [
            {'R_ID': respondent, self.code: answer.scale} if self.scale_encode else {'R_ID': respondent, self.code: answer.text} 
            for answer in self.answers 
            for respondent in answer.respondents
        ]
        
        df = pd.DataFrame(data)
        
        if self._ctab_mode:
            return df
        else:
            return df.set_index('R_ID')
    
    
    