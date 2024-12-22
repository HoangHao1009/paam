from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.shemas.config_schemas import ConfigSchema
from app.engine import QuestionPro
from app.db.redis import redis_client

import json


router = APIRouter()



@router.post("/")
async def set_config(config_schema: ConfigSchema):
    config = {
        'src_platform': config_schema.src_platform,
        'survey_id': config_schema.survey_id,
        'api_key': config_schema.api_key
    }
    
    redis_client.set('configuration', json.dumps(config))
    
    questionpro = QuestionPro(
        survey_id=config_schema.survey_id, 
        api_key=config_schema.api_key
    )
    
    await questionpro.fetch_data()
            
    data = {
        'survey_name': questionpro.name,
        'survey_data': questionpro.data
    }
    
    redis_client.set('survey_data', json.dumps(data), ex=3600)
    
    return JSONResponse(
        content={
            'message': 'Setting config successfully',
            'config': config
        },
        status_code=200
    )
