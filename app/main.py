from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis
import json

from .engine import QuestionPro, Survey

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_survey(survey_id: str):
    cached_survey = redis_client.get(survey_id)
    
    if cached_survey:
        data = json.loads(cached_survey)
        survey = Survey(data=data['survey_data'], name=data['name'])
        return {
            "message": "Survey loaded from cache",
            "survey_name": survey.name
        }
    else:
        return None

class SurveyRequest(BaseModel):
    survey_id: str
    api_key: str
    
@app.get("/")
async def home_page():
    return {"message": "HELLO"}

@app.post("/survey")
async def create_survey(survey_request: SurveyRequest):
    questionpro = QuestionPro(
        survey_id=survey_request.survey_id, 
        api_key=survey_request.api_key
    )
    
    await questionpro.fetch_data()
            
    data = {
        'survey_name': questionpro.name,
        'survey_data': questionpro.data
    }
    
    redis_client.set(survey_request.survey_id, json.dumps(data), ex=3600)    
    
    return JSONResponse(
        content={
            "message": "Survey created successfully",
            "survey_name": questionpro.name,
        },
        status_code=200
    )
