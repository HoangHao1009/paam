from typing import List, Literal, Union

class Answer:
    def __init__(self, id: str, scale: int, text: str, question: str, respondents: List[str]):
        self._id = id
        self.scale = scale
        self.text = text
        self.question = question
        self.respondents = respondents
        
    def __str__(self):
        return f"Answer(question: {self.question}), text: {self.text}, scale: {self.scale}, num_respondent: {len(self.respondents)}\n->respondents: {self.respondents}"
    
    def __repr__(self):
        return f"Answer(text: {self.text}, scale: {self.scale}"
    
    @property
    def code(self):
        return f"{self.question}_{self.scale}"
        
class Question:
    def __init__(self, id: str, code: str, text: str, order: int, type: str, answers: List[Answer] = []):
        self._id = id
        self.code = code
        self.text = text
        self.order = order
        self.type = type
        self.answers = answers
        
    @property
    def respondents(self):
        respondent_list = []
        for answer in self.answers:
            for respondent in answer.respondents:
                if respondent not in respondent_list:
                    respondent_list.append(respondent)
        return respondent_list
                
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
        