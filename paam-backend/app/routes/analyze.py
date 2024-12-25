from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.db.redis import get_redisdb, RedisCacheDB
from app.schemas.analyze_schemas import CrossTabSchema
from app.engine import Survey

router = APIRouter()

@router.post("/crosstab")
async def crosstab(crosstab_schema: CrossTabSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey = cache_db.get_survey()
    survey.initialize()
    
    crosstab = survey.crosstab(base=crosstab_schema.base, target=crosstab_schema.target, deep_by=crosstab_schema.deepBy)
    
    return JSONResponse(
        content={
            'crosstabData': crosstab.df.to_json()
        },
        status_code=200
    )