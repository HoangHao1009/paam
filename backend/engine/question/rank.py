from typing import List

from .core_question import Question, Answer
from .helper_function import _get_duplicates
from ..utils import spss_function

from .single import Single

class Rank(Question):
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer]):
        super().__init__(id, code, text, order, type, answers)
        # self._check_invalid()
    
    def _check_invalid(self):
        invalid = []
        for sa_question in self.decompose():
            respondents = []
            for answer in sa_question.answers:
                respondents.extend(answer.respondents)
            invalid.extend(_get_duplicates(respondents))
        if len(invalid) > 0:
            raise ValueError(f"Error - Duplicates occurs: {invalid}")
        
    @property
    def spss_syntax(self):
        value_label_dict = {index: response.text for index, response in enumerate(self.answers, 1)}
        var_label_command = []
        value_label_command = []

        for response in self.answers:
            code = response.code
            var_label = f"{self.text}_RANK{response.scale}"
            value_label = spss_function.value_label(code, value_label_dict)
            var_label_command.append(spss_function.var_label(code, var_label))
            value_label_command.append(value_label)
        return var_label_command + value_label_command

    def decompose(self):
        rank_set = {i.scale for i in self.answers}
        value_list = list({i.scale for i in self.answers})

        elements = [
            Single(
                id=f"{self._id}RANK{r}",
                code=f"{self.code}rank{r}",
                text=f"{self.text}_rank{r}",
                type="rank_decomposed",
            )
            for r in rank_set
        ]

        for element in elements:
            rank = int(element.code.split('rank')[-1])
            responses_by_value = {resp.text: resp for resp in self.answers if resp.scale == rank}
            for text, resp in responses_by_value.items():
                try:
                    response = element.get_answer(text, by='text')
                except:
                    response = None
                if response:
                    response.respondents.append(resp.respondents)
                else:
                    element.answers.append(
                        Answer(
                            id=f"{element._id}_{text}",
                            text=text,
                            scale=value_list.index(text),
                            question=element.code,
                            respondents=resp.respondents
                        )
                    )    
        return elements
    