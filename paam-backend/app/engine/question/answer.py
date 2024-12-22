from typing import List

class Answer:
    def __init__(self, id: str, scale: int, text: str, question: str, respondents: List[str], question_code=None):
        self._id = id
        self.scale = scale
        self.text = text
        self.question = question
        self.respondents = respondents
        self.question_code = question_code
        self.is_rank = False
        
    def __str__(self):
        return f"Answer(question: {self.question}), text: {self.text}, scale: {self.scale}, num_respondent: {len(self.respondents)}\n->respondents: {self.respondents}"
    
    def __repr__(self):
        return f"Answer(text: {self.text}, scale: {self.scale}"
    
    @property
    def code(self):
        return f"{self.question_code}_{self.scale}" if not self.is_rank else f"{self.question_code}RANK{self.scale}"
    
    def to_json(self):
        return {
            'answer_code': self.code,
            'answer_scale': self.scale,
            'answer_text': self.text,
            'answer_respondents': self.respondents,
        }
