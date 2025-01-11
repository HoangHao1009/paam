from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.db.redis import get_redisdb, RedisCacheDB
from app.schemas.process_schemas import QuestionComputeSchema, DeleteConstructionSchema

import ast

router = APIRouter()

@router.get("/survey_data")
async def read_survey_data(cache_db: RedisCacheDB=Depends(get_redisdb)):
    return JSONResponse(
        content={
            'surveyData': cache_db.get('survey_data')
        },
        status_code=200
    )
    
@router.post("/delete")
async def delete_compute_constructions(delete_schema: DeleteConstructionSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    compute_constructions = cache_db.get('compute_constructions')
    new_constructions = [
        construction for construction in compute_constructions
        if construction["newQuestionCode"] != delete_schema.questionCode
    ]
    cache_db.set('compute_constructions', new_constructions)
    
    return {"message": "Delete Success"}

@router.get("/questions")
async def read_questions(cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey = cache_db.get_survey()    
    question_json = [question.to_json(snake_case=False) for question in survey.questions]
    
    return JSONResponse(
        content = {
            'surveyName': cache_db.get('survey_name'),
            'questionData': question_json
        },
        status_code=200
    )
        
@router.post("/compute")
async def compute_question(compute_schema: QuestionComputeSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):    
    compute_construction = compute_schema.__dict__
    
    if cache_db.exists("compute_constructions"):
        cache_contruction = cache_db.get("compute_constructions")
        cache_contruction.append(compute_construction)
        cache_db.set("compute_constructions", cache_contruction)
        print(f"APPEND Construction: {compute_construction}")
    else:
        cache_db.set("compute_constructions", [compute_construction])
        print(f"SET Construction: {compute_construction}")
        
    print("CACHE CONTRUCTIONS", cache_db.get("compute_constructions"))
        
    return {"message": "Computed Success"}
    
