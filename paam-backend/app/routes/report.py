from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse

from app.db.redis import get_redisdb, RedisCacheDB
from app.engine import Survey
from app.schemas.report_shemas import ExportSettingSchema

router = APIRouter()

@router.post("/settings")
async def set_export(export_setting_schema: ExportSettingSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    
    export_settings = export_setting_schema.__dict__
    cache_db.set('export_settings', export_settings)
    
    return {
        'message': 'Setting export successfully',
        'settings': export_settings
    }
    
@router.post("/pptx_template")
async def set_pptx_template(file: UploadFile = File(...), cache_db: RedisCacheDB=Depends(get_redisdb)):
    try:
        file_location = f"/uploads/{file.filename}"
        cache_db.set("pptx_template_file_location", file_location)
        with open(file_location, "wb") as f:
            f.write(await file.read())
            
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error during file upload: {e}"}
        )

@router.get("/excel")
async def get_excel(cache_db: RedisCacheDB=Depends(get_redisdb)):
    export_settings = cache_db.get('export_settings')
    survey = cache_db.get_survey()
    survey.control_vars = export_settings['controlVars']
    survey.target_vars = export_settings['targetVars']
    survey.deep_vars = export_settings['deepVars']
    
    zip_buffer = survey.to_excel()
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=SurveyData.zip"}
    )

@router.get("/spss")
async def get_spss(cache_db: RedisCacheDB=Depends(get_redisdb)):
    export_settings = cache_db.get('export_settings')
    survey = cache_db.get_survey()
    survey.control_vars = export_settings['controlVars']
    survey.target_vars = export_settings['targetVars']
    survey.deep_vars = export_settings['deepVars']
        
    zip_buffer = survey.to_spss()
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=SurveyData.zip"}
    )

@router.get("/datasets")
async def get_excel(cache_db: RedisCacheDB=Depends(get_redisdb)):
    export_settings = cache_db.get('export_settings')
    survey = cache_db.get_survey()
    survey.control_vars = export_settings['controlVars']
    survey.target_vars = export_settings['targetVars']
    survey.deep_vars = export_settings['deepVars']
    
    zip_buffer = survey.to_datasets()
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=Datasets.zip"}
    )
    
@router.get("/pptx")
async def get_pptx(cache_db: RedisCacheDB=Depends(get_redisdb)):
    try:
        pptx_template_path = cache_db.get('pptx_template_file_location')
    except:
        pptx_template_path = ""
    export_settings = cache_db.get('export_settings')
    survey = cache_db.get_survey()
    survey.control_vars = export_settings['controlVars']
    survey.target_vars = export_settings['targetVars']
    survey.deep_vars = export_settings['deepVars']
    
    zip_buffer = survey.to_ppt(template_path=pptx_template_path)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=PPTX.zip"}
    )

