import pandas as pd

from .core_question import Question, Answer
from .helper_function import _get_duplicates
from ..utils import spss_function
from typing import List

class Multiple(Question):
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer]):
        super().__init__(id, code, text, order, type, answers)
        self.respondents = self._get_respondents()
        # self.ctab_mode = False
    
    def _get_respondents(self):
        invalid = []
        respondents = []
        for answers in self.answers:
            respondents.append(answers.respondents)
            duplicates = _get_duplicates(answers.respondents)
            invalid.extend(duplicates)
            
        if len(respondents) == 0:
            raise AttributeError(f"Question have no respondent")

        if len(invalid) > 0:
            raise ValueError(f"Error - Duplicates occurs: {invalid}")
        
        return respondents
        
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
    
    @property
    def df(self):
        data = [{'R_ID': respondent, 'answer': answer.code, 'value': 1}
                for answer in self.answers 
                for respondent in answer.respondents]
                
        df = pd.DataFrame(data).pivot(index='R_ID', columns='answer', values='value')
        
        desired_cols = [answer.code for answer in self.answers]
        missing_columns = [col for col in desired_cols if col not in df.columns]
        
        if missing_columns:
            for col in missing_columns:
                df[col] = 0
                
        df.sort_index(axis=1, key=lambda x: pd.Categorical(x, categories=desired_cols, ordered=True))
        
        return df.fillna(0)