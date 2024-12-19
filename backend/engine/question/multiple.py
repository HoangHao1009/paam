from .core_question import Question, Answer
from .helper_function import _get_duplicates
from ..utils import spss_function
from typing import List

class Multiple(Question):
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer]):
        super().__init__(id, code, text, order, type, answers)
        # self._check_invalid()
    
    def _check_invalid(self):
        invalid = []
        for answers in self.answers:
            duplicates = _get_duplicates(answers.respondents)
            invalid.extend(duplicates)
        
        if len(invalid) > 0:
            raise ValueError(f"Error - Duplicates occurs: {invalid}")
        
    @property
    def spss_syntax(self):
        var_label_command = []
        value_label_command = []

        for answer in self.answers:
            code = answer.code
            label = f'{self.text}_{answer.text}'

            var_label_command.append(spss_function.var_label(code, label))
            value_label_command.append(spss_function.value_label(code, {1: answer.text}))

        repsonses_code = [i.code for i in self.answers]

        mrset_command = spss_function.mrset(self.code, self.text, repsonses_code)

        return var_label_command + value_label_command + [mrset_command]
