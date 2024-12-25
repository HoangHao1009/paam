from typing import List, Literal, Union
from .answer import Answer
from ..utils import snake_to_camel
        
class Question:
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer] = []):
        self._id = id
        self.code = code
        self.text = text
        self.order = order
        self.type = type
        self.answers = answers
        self.respondents = []
        self._ctab_mode = False
                        
    def __str__(self):
        answers = ""
        for answer in self.answers:
            answers += f"        --> {answer.scale} - {answer.text} - num_respondent: {len(answer.respondents)}\n"
        describe = f"""
Question(code={self.code}, text={self.text}, type={self.type}, num_answers={len(self.answers)}, num_respondent={len(self.respondents)})
-> answers:
{answers}
-> respondents:
{self.respondents}
        """
        return describe
    
    def __repr__(self):
        return f"Question(code={self.code}, text={self.text}, type={self.type}, num_answers={len(self.answers)})"
        
    def get_answer(self, query, by: Literal['text', 'scale']) -> Answer:
        for answer in self.answers:
            compare_attr = answer.text if by == 'text' else answer.scale
            if query == compare_attr:
                return answer
        
        raise KeyError(f'Query: {query} can not be found')
    
    def sort_answer(self, sorted_list: List[Union[str, int]], by: Literal['text', 'scale'], drop: bool=False):
        if len(sorted_list) != len(self.answers) and drop == False:
            raise ValueError(f"Length of sorted_list is different with answers. Required to set drop=True.")
        
        new_answers = []
        for item in sorted_list:
            for answer in self.answers:
                compare_attr = answer.text if by == 'text' else answer.scale
                if item == compare_attr:
                    new_answers.append(answer)
                    break
        self.answers = new_answers
        
    def to_json(self, snake_case: bool=False):
        answers_json = [answer.to_json(snake_case) for answer in self.answers]
        question_json = {
            'question_code': self.code,
            'question_text': self.text,
            'question_type': self.type,
            'question_respondents': self.respondents,
            'question_answers': answers_json
        }
        if snake_case:
            return question_json
        else:
            return {snake_to_camel(key): value for key, value in question_json.items()}
