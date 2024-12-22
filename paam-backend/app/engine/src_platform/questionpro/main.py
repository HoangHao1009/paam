import asyncio
from typing import Dict, List
from copy import deepcopy

from ._fetching_utils import _fetch_by_urls

QUESTIONPRO_BASE_URL = "https://api.questionpro.com/a/api/v2/surveys/"

TYPE_CONVERT = {
    'sa': ['multiplechoice_radio', 'multiplechoice_dropdown', 'multiplechoice_smiley', 'lookup_table', 'text'],
    'sa_matrix': ['matrix_radio', 'matrix_dropdown', 'matrix_slider'],
    'ma': ['multiplechoice_checkbox'],
    'ma_matrix': ['matrix_checkbox'],
    'number': ['numeric_slider'],
    'rank': ['rank_order_dropdown', 'rank_order_drag_drop'],
    'unprocessed': ['text_multiple_row', 'text_single_row', 'contact_information', 'static_presentation_text',
                    'matrix_text'],
}

def find_type(raw_type):
    for new_type, old_type_list in TYPE_CONVERT.items():
        if raw_type in old_type_list:
            return new_type
    
    raise KeyError(f"Type: {raw_type} can not be convert to valid type")

def find_answer(answer_id: str, answer_list: List[dict]) -> dict:
    answer_id = str(answer_id) if not isinstance(answer_id, str) else answer_id
    for answer in answer_list:
        if str(answer['id']) == str(answer_id):
            return answer
        elif int(answer_id) == 0:
            return None
    
    raise KeyError(f'Answer id: {answer_id} can not be find')

def find_question(question_id: str, question_list: List[dict]) -> dict:
    question_id = str(question_id) if not isinstance(question_id, str) else question_id
    for question in question_list:
        if question['id'] == question_id:
            return question
    
    raise KeyError(f'Question id: {question_id} can not be find')

def process_rows(raw_question: dict, question_list: list, answer_list: list):
    type = find_type(raw_question['type'])
    onlyone_row = True if len(raw_question['rows']) == 1 else False
    for i, row in enumerate(raw_question['rows'], 1):
        code = raw_question['code'] if onlyone_row else f"{raw_question['code']}_{i}"
        text = row['text'] if onlyone_row else f"{raw_question['text']}_{row['text']}"
        new_question = {
            'id': str(row['rowID']),
            'code': code,
            'text': text,
            'order': raw_question['orderNumber'] + i/10,
            'type': type,
            'answers': [],
        }
        
        if 'columns' in row.keys():
            for i, col in enumerate(row['columns'], 1):
                id = str(col['columnID'])
                text = col['text'] if "text" in col.keys() else ""
                new_answer = {
                    'id': id,
                    'scale': i,
                    'text': text,
                    'question': new_question['id'],
                    'respondents': []
                }
                
                new_question['answers'].append(id)
                answer_list.append(new_answer)
        question_list.append(new_question)
    
def process_answers(raw_question: dict, question_list: list, answer_list: list):
    type = find_type(raw_question['type'])
    new_question = {
        'id': str(raw_question['questionID']),
        'code': raw_question['code'],
        'text': raw_question['text'],
        'order': raw_question['orderNumber'],
        'type': type,
        'answers': [],
    }
    
    if 'answers' in raw_question.keys():
        for answer in raw_question['answers']:
            id = str(answer['answerID'])
            new_answer = {
                'id': id,
                'scale': answer['orderNumber'],
                'text': answer['text'],
                'question': new_question['id'],
                'respondents': []
            }
            
            new_question['answers'].append(id)
            answer_list.append(new_answer)
    question_list.append(new_question)

class QuestionPro:
    # Fix fetch api by page more wisely
    """
    Return object for getting QuestionPro data
    
    Arguments:
    survey_id: id of specific survey. You can take it in QuestionPro Survey > Settings > Survey ID
    api_key: key for connect to QuestionPro endpoint. You can take it in QuestionPro Survey > Intergration > API
    """
    def __init__(self, survey_id: str, api_key: str):
        self.survey_id = survey_id
        self.api_key = api_key
        self.survey_url = QUESTIONPRO_BASE_URL + survey_id
        self.headers = {'api-key': self.api_key}
        
    async def fetch_data(self):
        """
        Fetch and store survey, question, and response data.
        This method should be called after the instance is created.
        """
        # Gọi bất đồng bộ các hàm lấy dữ liệu và đợi hoàn thành
        self.response = await self._get_response()
        self.data = await self._get_data()
        self.name = self.response['survey_data']['name'].replace(' ', '_').strip()

        # Trả về kết quả sau khi lấy xong dữ liệu
        return self.response, self.data
        
    async def _get_response(self) -> Dict[str, List[dict]]:
        """
        Return a dictionary of survey information:
        - survey data
        - question data
        - response data
        """
        result = {}
        
        survey_response = await _fetch_by_urls(self.survey_url, self.headers)
        result.update({'survey_data': survey_response[0]['response']})
        
        total_response = result['survey_data']['completedResponses'] + result['survey_data']['startedResponses']
        
        question_url = self.survey_url + f"/questions?page=1&perPage=100"
        question_response = await _fetch_by_urls(question_url, self.headers)
        result.update({'question_data': question_response[0]['response']})
        
        num_response_page = int(total_response/ 100) if total_response > 100 else 1
                
        response_urls = [self.survey_url + f'/responses?page={i}&perPage=100&languageID=250' for i in range(1, num_response_page+1)]
                
        response_response = await _fetch_by_urls(response_urls, self.headers)
        
        responses = []
        for page in response_response:
            if 'error' not in page['response']:
                responses.extend(page['response'])
        
        result.update({'response_data': responses})

        return result
    
    async def _get_data(self):
        "Return constructed object of questions, answers, respondents"
        question_list = []
        answer_list = []
        respondent_list = []
        
        #initialize question_list and answer_list
        for raw_question in self.response['question_data']:
            if 'phone' in raw_question.keys() or 'email' in raw_question.keys():
                raw_question['rows'] = [raw_question['phone'], raw_question['email']]
                new_question = {
                    'id': str(raw_question['questionID']),
                    'code': raw_question['code'],
                    'text': raw_question['text'],
                    'order': raw_question['orderNumber'],
                    'type': 'text',
                    'answers': [],
                }
                question_list.append(new_question)
            if 'rows' in raw_question.keys():
                process_rows(raw_question, question_list, answer_list)
            else:
                process_answers(raw_question, question_list, answer_list)
            
        #initialize respondent_list and connect with answer_list
        for response in self.response['response_data']:
            id = str(response['responseID'])
            new_respondent = {
                'id': id,
                'timestamp': response['timestamp'],
                'latitude': response['location']['latitude'],
                'longitude': response['location']['longitude'],
                'time_taken': response['timeTaken'],
                'status': response['responseStatus'],
                'custom_var': response['customVariables'],
            }
            for response_answer in response['responseSet']:
                root_question = find_question(response_answer['questionID'], question_list)
                for answer in response_answer['answerValues']:
                    if answer['answerID'] == 0:
                        continue
                    answer_values = answer['value']
                    
                    try:
                        root_answer = find_answer(answer['answerID'], answer_list)  
                    except:
                        id = str(answer['answerID'])
                        root_answer = {
                            'id': id,
                            'scale': len(root_question['answers']) + 1,
                            'text': '',
                            'question': root_question['id'],
                            'respondents': []
                        }
                        answer_list.append(root_answer)
                        root_question['answers'].append(id)
                        
                    root_answer['respondents'].append(id)
                    text = answer_values['other'] + answer_values['dynamicExplodeText'] + answer_values['text']
                    #create new oe question
                    have_text = True if str(text) != '' else False
                    if have_text:
                        suffix = f"T{root_answer['scale']}"
                        oe_question_id = f"{response_answer['questionID']}_{suffix}"
                        try:
                            oe_question = find_question(oe_question_id, question_list)
                        except:
                            root_question = find_question(response_answer['questionID'], question_list)
                            oe_question = {
                                'id': oe_question_id,
                                'code': f"{root_question['code']}{suffix}",
                                'text': f"{root_question['text']}_{root_answer['text']}",
                                'order': root_question['order'] + 0.01,
                                'type': 'text',
                                'answers': []
                            }
                            question_list.append(oe_question)
                        
                        new_oe_answer_scale = len(oe_question['answers']) + 1
                        new_oe_answer_id = f"{root_answer['id']}_{new_oe_answer_scale}"
                        
                        try:
                            oe_answer = find_answer(new_oe_answer_id, answer_list)
                            oe_answer['respondents'].append(id)
                        except:
                            reference_text = f"[{root_answer['text']}] {text}" if root_answer['text'] != '' else text
                            
                            oe_answer = {
                                'id': new_oe_answer_id,
                                'scale': new_oe_answer_scale,
                                'text': reference_text,
                                'question': oe_question_id,
                                'respondents': [id]
                            }
                            
                            answer_list.append(oe_answer)
                            
                        oe_question['answers'].append(new_oe_answer_id)
                                            
            respondent_list.append(new_respondent)
            
        unprocessed_questions = [question['id'] for question in question_list if question['type'] == 'unprocessed']
        question_list = [question for question in question_list if question['id'] not in unprocessed_questions]      
        
        answer_list = [answer for answer in answer_list if answer['question'] not in unprocessed_questions]
            
        return {
            'questions': question_list,
            'answers': answer_list,
            'respondents': respondent_list
        }
                    
                
                
    




            
                    
            



        

        
        
        
        
