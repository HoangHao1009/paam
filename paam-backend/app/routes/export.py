from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.db.redis import get_redisdb, RedisCacheDB
from app.engine import Survey
from app.schemas.export_schemas import ExportSettingSchema

router = APIRouter()

@router.post("/settings")
async def set_export(export_setting_schema: ExportSettingSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    
    export_settings = export_setting_schema.__dict__
    cache_db.set('export_settings', export_settings)
    
    return {
        'message': 'Setting export successfully',
        'settings': export_settings
    }

@router.get("/excel")
async def get_excel(cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey_data = cache_db.get('survey_data')
    export_settings = cache_db.get('export_settings')
    survey = Survey(
        data=survey_data,
        control_vars=export_settings['controlVars'],
        target_vars=export_settings['targetVars'],
        deep_vars=export_settings['deepVars'],
    )
    survey.initialize()
    
    zip_buffer = survey.to_excel()
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=SurveyData.zip"}
    )

@router.get("/spss")
async def get_excel(cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey_data = cache_db.get('survey_data')
    export_settings = cache_db.get('export_settings')
    survey = Survey(
        data=survey_data,
        control_vars=export_settings['controlVars'],
        target_vars=export_settings['targetVars'],
        deep_vars=export_settings['deepVars'],
    )
    survey.initialize()
    
    zip_buffer = survey.to_spss()
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=SurveyData.zip"}
    )
