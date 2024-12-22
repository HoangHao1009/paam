from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.engine import Survey
from app.db.redis import redis_client

import json
import redis


router = APIRouter()


@router.get("/dashboard")
async def read_dashboard():
    survey_data = json.loads(redis_client.get('survey_data'))
    survey = Survey(data=survey_data['survey_data'], name=survey_data['survey_name'])
    
    survey.initialize()
    
    question_json = [question.to_json() for question in survey.questions]
    
    return JSONResponse(
        content = {
            'survey_name': survey.name,
            'question_data': question_json
        },
        status_code=200
    )

