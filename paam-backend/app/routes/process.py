from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.db.redis import get_redisdb, RedisCacheDB

router = APIRouter()

@router.get("/questions")
async def read_questions(cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey = cache_db.get_survey()
    survey.initialize()
    
    question_json = [question.to_json(snake_case=False) for question in survey.questions]
    
    return JSONResponse(
        content = {
            'surveyName': cache_db.get('survey_name'),
            'questionData': question_json
        },
        status_code=200
    )
