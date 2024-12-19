from .core_question import Question, Answer
from .helper_function import _get_duplicates
from ..utils import spss_function
from .number import Number
from typing import List

class Single(Question):
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
        value_label_dict = {index: response.value for index, response in enumerate(self.answers, 1)}
        var_label_command = spss_function.var_label(code, self.text)
        value_label_command = spss_function.value_label(code, value_label_dict)
        return [var_label_command, value_label_command]
    
    def to_number(self) -> Number:
        return Number(**self.__dict__)
    
    