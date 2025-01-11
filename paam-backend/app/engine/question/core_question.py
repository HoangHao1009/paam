from typing import List, Literal, Union, Dict
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
        self.construct_dict = {}
        
    def get_describe(self):
        answers = ""
        for answer in self.answers:
            answers += f"        --> {answer.scale} - {answer.text} - num_respondent: {len(answer.respondents)}\n"
        describe = f"""
Question(code={self.code}, text={self.text}, type={self.type}, num_answers={len(self.answers)}, num_respondent={len(self.respondents)})
-> answers:
{answers}
        """
        return describe
                        
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
    
    @property
    def is_constructed(self):
        return True if self.construct_dict != {} else False
        
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
            'is_constructed': self.is_constructed,
            'construction': self.construct_dict,
            'question_answers': answers_json,
        }
        if snake_case:
            return question_json
        else:
            return {snake_to_camel(key): value for key, value in question_json.items()}
        
    def compute(
        self, construct_dict: Dict[str, List], 
        new_code: str,
        new_text: str=None,
        method: Literal['cluster', 'classify']='cluster',
        by: Literal['text', 'scale']='value',   
        order: int=0
    ):
        """
        Ex construct_dict: {
            "ab": ["a", "b"],
            "cd": ["c", "d"],
            "ed": ["e", "d"]
        }
        -> Method cluster: key is new label, value is list of old label.
        -> Method Classify: key is old label, value is list of new label.
        """
        from .multiple import Multiple
        from .single import Single
        
        if not isinstance(self, (Multiple, Single)):
            raise ValueError(f"Required Multitple or Single type. Invalid: {type(self)}")
        
        new_question_id = f"new_{self._id}_{new_code}"
        new_answers = []
        to_ma = True
        
        if method == "cluster":
            old_labels = [label for labels in construct_dict.values() for label in labels]
            to_ma = len(old_labels) != len(set(old_labels))
            
            new_answers = []
            
            for index, (new_label, old_label_list) in enumerate(construct_dict.items(), 1):
                new_respondents = []
                for old_label in old_label_list:
                    new_respondents.extend(self.get_answer(old_label, by=by).respondents)
                new_answer = Answer(
                    id=f"{new_question_id}_{index}", 
                    scale=index, text=new_label, question=new_question_id, 
                    question_code=new_code,
                    respondents=new_respondents
                )
                new_answers.append(new_answer)
                
        elif method == "classify":
            new_labels = list(set(label for labels in construct_dict.values() for label in labels))
            new_answers_mapping = {
                new_label: Answer(
                    id=f"{new_question_id}_{index}", 
                    scale=index, text=new_label, question=new_question_id, 
                    question_code=new_code,
                    respondents=[]
                )
                for index, new_label in enumerate(new_labels)
            }
            
            for index, (old_label, new_label_list) in enumerate(construct_dict.items(), 1):
                for new_label in new_label_list:
                    new_answer = new_answers_mapping[new_label]
                    new_answer.respondents.extend(self.get_answer(old_label, by=by).respondents)
            
            new_answers = new_answers_mapping.values()
                
        new_question_info = {
            "id": new_question_id,
            "code": new_code,
            "text": new_text if new_text else f"new_{self.text}_{new_code}",
            "order": order,
            "answers": new_answers,
        }
        
        if to_ma or isinstance(self, Multiple):
            new_question = Multiple(**new_question_info, type="ma")
        else:
            new_question = Single(**new_question_info, type="sa")
            
        new_question.construct_dict = construct_dict
            
        return new_question

    # def to_src_platform_data(self):
    #     question_data = {
    #         'id': self._id,
    #         'code': self.code,
    #         'text': self.text,
    #         'order': self.order,
    #         'type': self.type,
    #         'answers': [answer._id for answer in self.answers]
    #     }
        
    #     answers_data = []
    #     for answer in self.answers:
    #         answers_data.append({
    #             'id': answer._id,
    #             'scale': answer.scale,
    #             'text': answer.text,
    #             'question': answer.question,
    #             'respondents': answer.respondents,
    #         })
    #     return question_data, answers_data
