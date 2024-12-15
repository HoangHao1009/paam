import asyncio
from typing import Dict, List

from ._fetching_utils import _get_data

QUESTIONPRO_BASE_URL = "https://api.questionpro.com/a/api/v2/surveys/"

TYPE_CONVERT = {
    'sa': ['multiplechoice_radio', 'multiplechoice_dropdown', 'multiplechoice_smiley', 'matrix_slider', 'matrix_radio', 'matrix_dropdown', 'lookup_table'],
    'text': ['text_multiple_row', 'text_single_row'],
    'ma': ['multiplechoice_checkbox'],
    'ma_matrix': ['matrix_checkbox'],
    'text_matrix': ['matrix_text'],
    'number': ['numeric_slider'],
    'rank': ['rank_order_dropdown', 'rank_order_drag_drop']
}

def find_type(raw_type):
    for new_type, old_type_list in TYPE_CONVERT.items():
        if raw_type in old_type_list:
            return new_type
    
    raise KeyError(f"Type: {raw_type} can not be convert to valid type")

def find_answer(answer_id: str, answer_list: List[dict]):
    for answer in answer_list:
        if answer['id'] == answer_id:
            return answer
    
    raise KeyError(f'Answer id: {answer_id} can not be find')

class QuestionPro:
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
        
    @property
    def response(self) -> Dict[str, List[dict]]:
        """
        Return a dictionary of survey information:
        - survey data
        - question data
        - response data
        """
        result = {}
        
        survey_response = asyncio.run(_get_data(self.survey_url, self.headers))
        result.update({'survey_data': survey_response[0]['response']})
        
        total_response = result['survey_data']['completedResponses'] + result['survey_data']['startedResponses']
        
        question_url = self.survey_url + f"/questions?page=1&perPage=100"
        question_response = asyncio.run(_get_data(question_url, self.headers))
        result.update({'question_data': question_response[0]['response']})
        
        num_response_page = int(total_response/ 100) if total_response > 100 else 1
                
        response_urls = [self.survey_url + f'/responses?page={i}&perPage=100&languageID=250' for i in range(1, num_response_page+1)]
        
        response_response = asyncio.run(_get_data(response_urls, self.headers))
        result.update({'response_data': response_response[0]['response']})

        return result
    
    @property
    def data(self):
        "Return constructed object of questions, answers, respondents"
        question_list = []
        answer_list = []
        respondent_list = []
        
        #initialize question_list and answer_list
        for raw_question in self.response['question_data']:
            type = find_type(raw_question['type'])
            if 'rows' in raw_question.keys():
                for i, row in enumerate(raw_question['rows'], 1):
                    new_question = {
                        'id': row['rowID'],
                        'code': f"{raw_question['code']}_{i}",
                        'text': f"{raw_question['text']}_{row['text']}",
                        'order': raw_question['orderNumber'] + i/10,
                        'type': type,
                        'answers': [],
                    }
                    
                    for i, col in enumerate(row['columns'], 1):
                        id = col['columnID']
                        text = col['text'] if "text" in col.keys() else ""
                        new_answer = {
                            'id': id,
                            'scale': i,
                            'text': text,
                            'question': new_question['id'],
                            'have_text': False,
                            'responses': []
                        }
                        
                        new_question['answers'].append(id)
                        answer_list.append(new_answer)
            else:
                new_question = {
                    'id': raw_question['questionID'],
                    'code': raw_question['code'],
                    'text': raw_question['text'],
                    'order': raw_question['orderNumber'],
                    'type': type,
                    'answers': [],
                }
                
                if 'answers' in raw_question.keys():
                    for answer in raw_question['answers']:
                        id = answer['answerID']
                        new_answer = {
                            'id': id,
                            'scale': answer['orderNumber'],
                            'text': answer['text'],
                            'question': new_question['id'],
                            'have_text': False,
                            'responses': []
                        }
                        
                        new_question['answers'].append(id)
                        answer_list.append(new_answer)

            
            question_list.append(new_question)
            
        #initialize respondent_list and connect with answer_list
        for response in self.response['response_data']:
            id = response['responseID']
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
                for answer in response_answer['answerValues']:
                    answer_values = answer['value']
                    text = answer_values['other'] + answer_values['dynamicExplodeText'] + answer_values['text']
                             
                    new_answer = find_answer(answer['answerID'], answer_list)
                        
                    new_answer['responses'].append({
                        'respondent': id,
                        'text': text,
                    })
                    
                    if str(text) != '':
                        new_answer['have_text'] = True
                                            
            respondent_list.append(new_respondent)
            
        return {
            'questions': question_list,
            'answers': answer_list,
            'respondents': respondent_list
        }
                    
                
                
    




            
                    
            



        

        
        
        
        
