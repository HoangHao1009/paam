import pandas as pd
from typing import Union, List

from ..question import Single, Multiple, Number, Rank, Answer
from ..src_platform import QuestionPro

question_type = Union[Single, Multiple, Number, Rank]

class Survey:
    def __init__(self, src_platform: Union[QuestionPro]):
        self.src_platform = src_platform
        self.data = src_platform.data
        self.questions: List[question_type] = self._get_questions()
        self._check_valid()
        
    @property
    def question_code_mapping(self):
        return {question.code: question for question in self.questions}
        
    def _check_valid(self):
        list_question_code = [question.code for question in self.questions]
        if len(list_question_code) != len(set(list_question_code)):
            seen = set()
            duplicates = set()
            for i in list_question_code:
                if i in seen:
                    duplicates.add(i)
                else:
                    seen.add(i)
            raise KeyError(f'Question code: {list(duplicates)} duplicated')
        
    def _get_questions(self):
        answer_lookup = {answer['id']: answer for answer in self.data['answers']}
        all_questions = []
        for question_data in self.data['questions']:
            answers = []
            for answer_id in question_data['answers']:
                answer_data = answer_lookup[answer_id]
                answer = Answer(**answer_data, question_code=question_data['code'])
                answer.is_rank = True if question_data['type'] == 'rank' else False
                answers.append(answer)
                
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
            
        all_questions.sort(key=lambda item: item.order) 
        
        return all_questions
        
    def get_question(self, key: Union[List[str], str]):
        """
        Getting questions by question code
        Arguments:
        - key: list or str of question code
        Return:
        List or single question object
        """
        if isinstance(key, str):
            if key in self.question_code_mapping:
                return self.question_code_mapping[key]
            else:
                raise KeyError(f"Question code {key} cannot be found")
        else:
            questions = []
            for question_code in key:
                if question_code in self.question_code_mapping:
                    questions.append(self.question_code_mapping[question_code])
                else:
                    raise KeyError(f"Question code {question_code} cannot be found")
            return questions
        
    def __getitem__(self, key: Union[List[str], str]):
        return self.get_question(key)
    
    def add_question(self, question_obj: question_type):
        if question_obj.code in self.question_code_mapping:
            raise KeyError(f"Question code: {question_obj} has been existed in survey")
        question_order = [question.order for question in self.questions]
        if question_obj.order in question_order:
            raise ValueError(f"Question code {question_obj.code} order: {question_obj.order} has been existed in survey")
        self.questions.append(question_obj)
        
    @property
    def df(self):
        dfs = [question.df for question in self.questions]
        return pd.concat(dfs, axis=1)
        