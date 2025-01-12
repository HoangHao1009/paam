from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse

from app.schemas.create_schemas import ConfigSchema, CreateSchema
from app.engine import QuestionPro
from app.engine.utils import snake_to_camel
from app.db.redis import get_redisdb, RedisCacheDB

from langchain_openai import ChatOpenAI
from app.engine.ai import QuestionnaireCreator, Extract_Chain

import os

router = APIRouter()

@router.post("/provider")
async def set_config(config_schema: ConfigSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    config = {
        'src_platform': config_schema.srcPlatform,
        'survey_id': config_schema.surveyId,
        'api_key': config_schema.apiKey
    }
    
    cache_db.set('configuration', config)
    
    if config_schema.surveyId != "":
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

llm = ChatOpenAI(model='gpt-3.5-turbo', streaming=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), cache_db: RedisCacheDB=Depends(get_redisdb)):
    try:
        file_location = f"/uploads/{file.filename}"
        cache_db.set("design_file_location", file_location)
        with open(file_location, "wb") as f:
            f.write(await file.read())
            
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error during file upload: {e}"}
        )

@router.post("/create")
async def create_questionnaire(request: CreateSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    print("Create Request:", request)
    survey_config = cache_db.get("configuration")
    
    extraction_chain = Extract_Chain(api_key=os.environ.get("OPENAI_API_KEY"))

    creator = QuestionnaireCreator(
        questionnaire_design_path=cache_db.get("design_file_location"), 
        extract_chain=extraction_chain, 
        api_key=survey_config["api_key"]
    )
    
    creator.create(request.surveyId)
    
    return {"message": "Questionnaire created successfully"}
