from typing import Union
from ..question import Single, Multiple, Number, Rank, Answer

from ..src_platform import QuestionPro


class Survey:
    def __init__(self, src_platform: Union[QuestionPro]):
        self.src_platform = src_platform
        self.data = src_platform.data
        self.questions = self._get_questions()
        
    def _get_questions(self):
        answer_lookup = {answer['id']: answer for answer in self.data['answers']}
        all_questions = []
        for question_data in self.data['questions']:
            answers = []
            for answer_id in question_data['answers']:
                answer_data = answer_lookup[answer_id]
                answers.append(Answer(**answer_data))
                
            question_data['answers'] = answers
                
            if question_data['type'] in ['sa', 'sa_matrix', 'text']:
                question = Single(**question_data)
            elif question_data['type'] in ['ma', 'ma_matrix']:
                question = Multiple(**question_data)
            elif question_data['type'] in ['number']:
                question = Number(**question_data)
            elif question_data['type'] in ['rank']:
                question = Rank(**question_data)
            else:
                raise ValueError(f"Question with id: {question_data['id']} code: {question_data['code']} with type: {question_data['type']} can not be processed")
            
            question.sort_answer(list(range(1, len(question.answers) + 1)), by='scale')
            
            all_questions.append(question)
            
        return all_questions