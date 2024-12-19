from .core_question import Question, Answer
from .helper_function import _get_duplicates
from ..utils import spss_function
from typing import List

class Number(Question):
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer]):
        super().__init__(id, code, text, order, type, answers)
        # self._check_invalid()
    
    def _check_invalid(self):
        respondents = []
        for answers in self.answers:
            respondents.extend(answers.respondents)
        invalid = _get_duplicates(respondents)
        
        if len(invalid) > 0:
            raise ValueError(f"Error - Duplicates occurs: {invalid}")
        
    @property
    def spss_syntax(self):
        code = self.code
        to_scale = f'VARIABLE LEVEL {code} (SCALE).'
        return [spss_function.var_label(code, self.text), to_scale]