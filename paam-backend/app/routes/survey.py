from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.schemas.config_schemas import ConfigSchema
from app.engine import QuestionPro, Survey
from app.engine.utils import snake_to_camel
from app.db.redis import get_redisdb, RedisCacheDB

router = APIRouter()

@router.post("/")
async def set_config(config_schema: ConfigSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    config = {
        'src_platform': config_schema.srcPlatform,
        'survey_id': config_schema.surveyId,
        'api_key': config_schema.apiKey
    }
    
    cache_db.set('configuration', config)
    
    questionpro = QuestionPro(
        survey_id=config_schema.surveyId, 
        api_key=config_schema.apiKey
    )
    
    await questionpro.fetch_data()
            
    data = questionpro.data
    
    cache_db.set('survey_data', data)
    cache_db.set('survey_name', questionpro.name)
    
    return JSONResponse(
        content={
            'message': 'Setting config successfully',
            'config': {snake_to_camel(key): value for key, value in config.items()},
        },
        status_code=200
    )

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
    
@router.get("/stats")
async def read_stats(cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey_data = cache_db.get('survey_data')
    survey = Survey(data=survey_data)
    survey.initialize()
    
    stats = survey.stats
    
    return JSONResponse(
        content = {
            'stats': stats,
        },
        status_code=200
    )
